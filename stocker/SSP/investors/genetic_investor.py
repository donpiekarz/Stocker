import collections

from stocker.common.events import EventStockOpen, EventStockClose, EventStockTransaction
from stocker.SSP.investors.base_investor import BaseInvestor

from pyevolve import G1DList
from pyevolve import GSimpleGA
from pyevolve import GAllele
from pyevolve import Consts
from pyevolve import Selectors
import mdp, random, numpy
import math
import functools

import talib

INDICES_NUMBER = 9

class IndicesContainer:
    def __init__(self, low_prices, high_prices, close_prices, volumes):
        self.indicesList = [SMAIndex(close_prices),
                            EMAIndex(close_prices),
                            MACDIndex(close_prices),
                            RSIIndex(close_prices),
                            STOCHRSIIndex(close_prices),
                            BBANDSIndex(close_prices),
                            ADXIndex(low_prices, high_prices, close_prices),
                            STOCHIndex(low_prices, high_prices, close_prices),
                            #ADOSCIndex(low_prices, high_prices, close_prices, volumes),
                            MFIIndex(low_prices, high_prices, close_prices, volumes)]

    def computeIndices(self):
        for index in self.indicesList:
            index.computeIndex()

    def getIndicesList(self):
        return self.indicesList


class ClosePriceIndexBase:
    def __init__(self, prices):
        self.prices = prices
        self.n = len(prices)
        self.result = 0

    def computeIndex(self):
        pass

    def getResult(self):
        return self.result


class AllPricesIndexBase:
    def __init__(self, low_prices, high_prices, close_prices):
        self.low_prices = low_prices
        self.high_prices = high_prices
        self.close_prices = close_prices
        self.n = len(low_prices)
        self.result = 0

    def computeIndex(self):
        pass

    def getResult(self):
        return self.result


class AllPricesAndVolumeIndexBase():
    def __init__(self, low_prices, high_prices, close_prices, volumes):
        self.low_prices = low_prices
        self.high_prices = high_prices
        self.close_prices = close_prices
        self.volumes = volumes
        self.n = len(low_prices)
        self.result = 0

    def computeIndex(self):
        pass

    def getResult(self):
        return self.result


class SMAIndex(ClosePriceIndexBase):
    def computeIndex(self):
        output = talib.SMA(self.prices)
        self.result = output
        return self.result


class EMAIndex(ClosePriceIndexBase):
    def computeIndex(self):
        output = talib.EMA(self.prices)
        self.result = output
        return self.result


class MACDIndex(ClosePriceIndexBase):
    def computeIndex(self):
        upper, middle, lower = talib.MACD(self.prices)
        self.result = middle
        return self.result


class RSIIndex(ClosePriceIndexBase):
    def computeIndex(self):
        output = talib.RSI(self.prices)
        self.result = output
        return self.result


class STOCHRSIIndex(ClosePriceIndexBase):
    def computeIndex(self):
        upper, lower = talib.STOCHRSI(self.prices)
        self.result = upper
        return self.result


class BBANDSIndex(ClosePriceIndexBase):
    def computeIndex(self):
        upper, middle, lower = talib.BBANDS(self.prices, matype=talib.MA_T3)
        self.result = middle
        return self.result


class ADXIndex(AllPricesIndexBase):
    def computeIndex(self):
        output = talib.ADX(self.high_prices, self.low_prices, self.close_prices)
        self.result = output
        return self.result


class STOCHIndex(AllPricesIndexBase):
    def computeIndex(self):
        upper, lower = talib.STOCH(self.high_prices, self.low_prices, self.close_prices)
        self.result = upper
        return self.result


class MFIIndex(AllPricesAndVolumeIndexBase):
    def computeIndex(self):
        output = talib.MFI(self.high_prices, self.low_prices, self.close_prices, self.volumes)
        self.result = output
        return self.result


class ADOSCIndex(AllPricesAndVolumeIndexBase):
    def computeIndex(self):
        output = talib.ADOSC(self.high_prices, self.low_prices, self.close_prices, self.volumes)
        self.result = output
        return self.result


class indicesNormalizer(object):
    def normalize(self, indices_values):
        highest_non_nan = 0
        for indexlist in indices_values:
            for element in range(len(indexlist)):
                if math.isnan(indexlist[element]):
                    if element > highest_non_nan:
                        highest_non_nan = element
                else:
                    break
                    #print "Highest non nan:", highest_non_nan

        normalized_list = []
        for indexlist in indices_values:
            normalized_list.append(indexlist[highest_non_nan + 1:])

        return normalized_list


def pickIndices(pickFrom, templateIndicesSet):
    result = []

    for index in pickFrom:
        for template_index in templateIndicesSet:
            if index.__class__.__name__ == template_index.__class__.__name__:
                result.append(index)
                break

    return result


class TrendFinderException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


def findSellTrendBeginning(close_prices, jump_limit=float('inf')):
    assert(len(close_prices))
    prev_price = close_prices[0]
    max_jump = 0
    max_jump_ind = 0

    for i in range(len(close_prices)):
        if close_prices[i] - prev_price > max_jump and math.fabs(close_prices[i] - prev_price < jump_limit):
            max_jump = close_prices[i] - prev_price
            max_jump_ind = i
        prev_price = close_prices[i]

    if max_jump_ind - 1 < 0:
        raise TrendFinderException("Couldn't find desired trend!")

    return max_jump_ind - 1 # because the indices, that can be used to determine the jump, can be computed from the previous price


def findBuyTrendBeginning(close_prices, jump_limit=float('inf')):
    prev_price = close_prices[0]
    max_jump = 0
    max_jump_ind = 0

    for i in range(len(close_prices)):
        if close_prices[i] - prev_price < max_jump and math.fabs(close_prices[i] - prev_price) < jump_limit:
            max_jump = close_prices[i] - prev_price
            max_jump_ind = i
        prev_price = close_prices[i]

    if max_jump_ind - 1 < 0:
        raise TrendFinderException("Couldn't find desired trend!")

    return max_jump_ind - 1 # because the indices, that can be used to determine the jump, can be computed from the previous price


class nonNanTrendFinder(object):
    def utilize(self, trendFinderfunctor, indices_list):
        retry_counter = 1
        trendBeginning = trendFinderfunctor()

        isNonNanVector = True
        for index in indices_list:
            if math.isnan(index.getResult()[trendBeginning]):
                isNonNanVector = False
                break

        while isNonNanVector == False:
            if retry_counter == 10:
                raise TrendFinderException("Couldn't find desired trend!")
            else:
                print trendBeginning
                print math.fabs(
                    trendFinderfunctor.args[0][trendBeginning + 1] - trendFinderfunctor.args[0][trendBeginning])
                trendBeginning = trendFinderfunctor.func(trendFinderfunctor.args[0],
                    math.fabs(
                        trendFinderfunctor.args[0][trendBeginning + 1] - trendFinderfunctor.args[0][trendBeginning]))
                isNonNanVector = True
                for index in indices_list:
                    if math.isnan(index.getResult()[trendBeginning]):
                        isNonNanVector = False
                        break
            retry_counter += 1

        return trendBeginning


class simpleTrendBeginningsFinder(object):
    def __init__(self, close_prices, indices_list):
        assert(len(close_prices))
        self.close_prices = close_prices
        self.indices_list = indices_list

    def findTrendBeginnings(self):
        sellTrendFunctor = functools.partial(findSellTrendBeginning, self.close_prices)
        buyTrendFunctor = functools.partial(findBuyTrendBeginning, self.close_prices)
        nonNanSellTrendBeginning = nonNanTrendFinder().utilize(sellTrendFunctor, self.indices_list)
        nonNanBuyTrendBeginning = nonNanTrendFinder().utilize(buyTrendFunctor, self.indices_list)

        return (nonNanSellTrendBeginning, nonNanBuyTrendBeginning)


def G1DListStockInitializator(genome, **args):
    genome.clearList()
    alleles = genome.getParam("allele")
    for element in random.sample(alleles[0], random.randint(1, INDICES_NUMBER)):
        genome.append(element)


def G1DListStockMutator(genome, **args):
    if random.uniform(0, 1.0) <= args['pmut']:
        current_genome = genome.getInternalList()
        full_genome = genome.getParam("allele")[0]
        if len(current_genome) == len(full_genome):
            return 0
        genome_difference = list(set(full_genome).difference(current_genome))

        rand_range = min(len(current_genome), len(genome_difference))
        j = random.randint(1, rand_range)

        exchange_set_full = random.sample(genome_difference, j)
        exchange_set_current = random.sample(current_genome, j)

        new_chromosome = []
        new_chromosome.extend(list(set(current_genome).difference(exchange_set_current)))
        new_chromosome.extend(exchange_set_full)
        genome.setInternalList(new_chromosome)

    return 0


def G1DListStockCrossoverOperator(genome, **args):
    dad_genome = args['dad'].getInternalList()
    mom_genome = args['mom'].getInternalList()

    intersection = list(set(dad_genome).intersection(set(mom_genome)))

    if len(intersection) == len(dad_genome) or len(intersection) == len(mom_genome):
    #if set(intersection) == set(dad_genome) or set(intersection) == set(mom_genome):
        return args['dad'].clone(), args['mom'].clone()

    child_1 = args['dad'].clone()
    child_2 = args['dad'].clone()
    child_1.clearList()
    child_2.clearList()

    rand_range = min(len(dad_genome), len(mom_genome)) - len(intersection)
    j = random.randint(1, rand_range)

    subset_dad = random.sample(list(set(dad_genome).difference(intersection)), j)
    subset_mom = random.sample(list(set(mom_genome).difference(intersection)), j)

    new_chromosome_1 = []
    new_chromosome_1.extend(intersection)
    new_chromosome_1.extend(subset_mom)
    child_1.setInternalList(new_chromosome_1)

    new_chromosome_2 = []
    new_chromosome_2.extend(intersection)
    new_chromosome_2.extend(subset_dad)
    child_2.setInternalList(new_chromosome_2)

    return child_1, child_2


def calculate_centroid_center(pca_results, data_points):
    center = []
    #computing coordinates

    for vector in pca_results:
        coordinate = 0
        for i in range(len(vector)):
            for j in range(len(data_points[i])):
                if not math.isnan(data_points[i][j]):
                    coordinate += vector[i] * data_points[i][j]
        center.append(coordinate / len(data_points[0]))
    return center


def eval_func(chromosome):
    """ The evaluation function """
    indices_values = []
    sellTrendVector = []
    buyTrendVector = []

    for gene in chromosome:
        indices_values.append(gene.getResult())
        sellTrendVector.append(gene.getResult()[:tradingGA.sellTrendBeginning])
        buyTrendVector.append(gene.getResult()[:tradingGA.buyTrendBeginning])

    #raw_input("Press ENTER to exit")

    indices_values = indicesNormalizer().normalize(indices_values)
    indices_values = numpy.asarray(indices_values)

    result = mdp.pca(indices_values.T, reduce=True)#, svd=True)
    sell_center = calculate_centroid_center(result[:4], sellTrendVector)
    buy_center = calculate_centroid_center(result[:4], buyTrendVector)

    #print sell_center, len(sell_center)
    #print buy_center, len(buy_center)

    wynik = numpy.linalg.norm(numpy.asarray(sell_center) - numpy.asarray(buy_center))

    return wynik


def computeClusterCentre(chromosome, trendBeginning):
    indices_values = []
    trendVector = []

    for gene in chromosome:
        indices_values.append(gene.getResult())
        trendVector.append(gene.getResult()[:trendBeginning])

    indices_values = indicesNormalizer().normalize(indices_values)
    indices_values = numpy.asarray(indices_values)

    result = mdp.pca(indices_values.T, reduce=True)
    center = calculate_centroid_center(result[:4], trendVector)

    return center


class tradingGA:
    sellTrendBeginning = 0
    buyTrendBeginning = 0

    def __init__(self, training_low_prices, training_high_prices, training_close_prices, training_volumes,
                 prediction_low_prices, prediction_high_prices, prediction_close_prices, prediction_volumes,
                 population_size=40, generations=50):
        print "Low prices: ", len(training_low_prices)
        print "High prices: ", len(training_high_prices)
        print "Close prices: ", len(training_close_prices)
        print "Volumes: ", len(training_volumes)
        self.training_low_prices = numpy.asarray(training_low_prices)
        self.training_high_prices = numpy.asarray(training_high_prices)
        self.training_close_prices = numpy.asarray(training_close_prices)
        self.training_volumes = numpy.asarray(training_volumes)

        self.prediction_low_prices = numpy.asarray(prediction_low_prices)
        self.prediction_high_prices = numpy.asarray(prediction_high_prices)
        self.prediction_close_prices = numpy.asarray(prediction_close_prices)
        self.prediction_volumes = numpy.asarray(prediction_volumes)

        self.population_size = population_size
        self.generations = generations

        #print sellTrend
        #print buyTrend
        #print close_prices

    def generateDecision(self):
        setOfAlleles = GAllele.GAlleles(homogeneous=True)
        #raw_input("Press ENTER to exit")
        # prepare indices

        print "Preparing indices..."

        indicesContainer = IndicesContainer(self.training_low_prices, self.training_high_prices,
            self.training_close_prices, self.training_volumes)
        indicesContainer.computeIndices()
        indicesList = indicesContainer.getIndicesList()

        # prepare sell trend and buy trend vectors

        print "Preparing sell trend and buy trend vectors..."

        #normalizedIndicesList = indices.indicesNormalizer().normalize(indicesContainer.getIndicesList())
        tradingGA.sellTrendBeginning, tradingGA.buyTrendBeginning = simpleTrendBeginningsFinder(
            self.training_close_prices, indicesList).findTrendBeginnings()
        print tradingGA.sellTrendBeginning
        print tradingGA.buyTrendBeginning

        # prepare individual

        print "Preparing first individual..."

        a = GAllele.GAlleleList(indicesList)
        setOfAlleles.add(a)

        genome = G1DList.G1DList()
        genome.setParams(allele=setOfAlleles)

        genome.evaluator.set(eval_func)
        genome.mutator.set(G1DListStockMutator)
        genome.crossover.set(G1DListStockCrossoverOperator)
        genome.initializator.set(G1DListStockInitializator)

        # prepare engine

        print "Preparing Genetic Algorithm engine..."

        ga = GSimpleGA.GSimpleGA(genome)
        ga.setGenerations(self.generations)
        ga.setMinimax(Consts.minimaxType["maximize"])
        ga.setCrossoverRate(1.0)
        ga.setMutationRate(0.1)
        ga.setElitismReplacement(3)
        ga.selector.set(Selectors.GUniformSelector)
        ga.setPopulationSize(self.population_size)

        print "Executing indices subset search..."

        ga.evolve(freq_stats=1)
        best = ga.bestIndividual()
        print best

        print "Generating trading signal..."

        print "Preparing prediction set indices..."

        predictionIndicesContainer = IndicesContainer(self.prediction_low_prices, self.prediction_high_prices,
            self.prediction_close_prices, self.prediction_volumes)
        predictionIndicesContainer.computeIndices()
        predictionIndicesList = predictionIndicesContainer.getIndicesList()

        # prepare sell trend and buy trend vectors

        print "Preparing prediction set sell trend and buy trend vectors..."

        sell = computeClusterCentre(best.getInternalList(), tradingGA.sellTrendBeginning)
        buy = computeClusterCentre(best.getInternalList(), tradingGA.buyTrendBeginning)
        predictionIndicesList = pickIndices(predictionIndicesList, best.getInternalList())
        prediction = computeClusterCentre(predictionIndicesList,
            len(predictionIndicesList[0].getResult())) #trend beginning to ostatni element listy z danymi

        d1 = numpy.linalg.norm(numpy.asarray(buy) - numpy.asarray(prediction))
        d2 = numpy.linalg.norm(numpy.asarray(sell) - numpy.asarray(prediction))

        print "d1", d1
        print "d2", d2

        if d1 < d2:
            print "Time for Buyin'"
        elif d1 > d2:
            print "Time for Sellin'"


class GeneticInvestor(BaseInvestor):
    MAX_INT = 100000

    learning = 0
    cash = 0

    companies = {}
    days = 0

    min_price_list = collections.defaultdict(list)
    max_price_list = collections.defaultdict(list)
    last_price_list = collections.defaultdict(list)
    volume_list = collections.defaultdict(list)

    min_price = collections.defaultdict(lambda: GeneticInvestor.MAX_INT)
    max_price = collections.defaultdict(lambda: 0)
    last_price = collections.defaultdict(lambda: None)
    volume = collections.defaultdict(lambda: 0)

    ga = collections.defaultdict(lambda: None)

    def process(self, event):
        #print event
        if isinstance(event, EventStockOpen):
            for company in self.companies.keys():
                self.volume[company] = 0
                self.last_price[company] = None
                self.min_price[company] = GeneticInvestor.MAX_INT
                self.max_price[company] = 0
                if self.learning <= self.days:
                    self.ga[company] = tradingGA(
                        self.min_price_list[company][:self.days], self.max_price_list[company][:self.days],
                        self.last_price_list[company][:self.days], self.volume_list[company][:self.days],
                        self.min_price_list[company][self.days:], self.max_price_list[company][self.days:],
                        self.last_price_list[company][self.days:], self.volume_list[company][self.days:]
                    )

        elif isinstance(event, EventStockClose):
            self.days += 1

            for company in self.companies.keys():
                if not self.last_price[company] is None:
                    self.min_price_list[company].append(self.min_price[company])
                    self.max_price_list[company].append(self.max_price[company])
                    self.last_price_list[company].append(self.last_price[company])
                    self.volume_list[company].append(self.volume[company])

        elif isinstance(event, EventStockTransaction):
            company = event.buy_order.company_id
            self.companies[company] = 1

            self.volume[company] += event.buy_order.amount
            self.last_price[company] = event.buy_order.limit_price
            self.max_price[company] = max(self.max_price[company], event.buy_order.limit_price)
            self.min_price[company] = min(self.min_price[company], event.buy_order.limit_price)
            
            
                
            
        