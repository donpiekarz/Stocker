
import collections

from stocker.common.events import EventStockOpen, EventStockClose, EventStockTransaction
from stocker.SSP.investor import Investor

class GA( object ):
    def __init__(self, min_price_list, max_price_list, last_price_list, volume_list):
        self.min_price_list = min_price_list
        self.max_price_list = max_price_list
        self.last_price_list = last_price_list
        self.volume_list = volume_list
        
        
        print min_price_list
        print max_price_list
        print last_price_list
        print volume_list

class GeneticInvestor( Investor ):
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
                    self.ga[company] = GA(self.min_price_list[company], self.max_price_list[company], self.last_price_list[company], self.volume_list[company])
                
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
            
            
                
            
        