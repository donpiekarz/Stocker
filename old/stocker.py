#!/usr/bin/python
"""
Stocker is a tool for stock exchange analysis
"""

__author__ = 'Mateusz Lis'
__version__ = '0.1'

# std imports 
from optparse import OptionParser
from random import random
import sys
from time import time

# local project imports 
from InvestmentStrategies import *
from StockData import StockData

def main(argv=None):
    global options 
    options = parseCommandLine()
    startTime = time()
    results = []
    printResult = True # print only results of first iteration
    fileMode = "w"
    
    for i in range( 2000 ):
        inv = globals()[ options.strategy ]()
        start = 85
        end = -1
        with open( options.dataFile ) as dataFile: 
            with open( options.outputFile, fileMode ) as outputFile:
                data = dataFile.readlines()
                name, date, openPrice, highPrice, lowPrice, firstClosePrice, vol = data[start].split( "\t" )
                name, date, openPrice, highPrice, lowPrice, lastClosePrice, vol = data[end].split( "\t" )
                firstClosePrice, lastClosePrice = float( firstClosePrice ), float( lastClosePrice )
                for line in data[ start:end ]:
                    if line[0] == "<":
                        continue
                    name, date, openPrice, highPrice, lowPrice, closePrice, vol = line.split( "\t" )
                    data = StockData( name, date, openPrice, highPrice, lowPrice,
                            closePrice, vol )
                    #print date, closePrice
                    if printResult:
                        outputFile.write( repr( inv.next( data ) ) )
                    else:
                        inv.next( data )
                results.append( inv.getBalance() )
        printResult = False
        fileMode = "r"

    print "Financial result", sum( results ) / float( len( results ) )
    print "Price increase", 1000 * ( lastClosePrice / firstClosePrice )
    if options.verbose:
        print "Execution time", time() - startTime
    


def parseCommandLine():
    """
    Sets up command line arguments and parses them
    """
    parser = OptionParser(usage="%prog ", version="%prog " + __version__,
                          description='''
    Stocker is a tool for stock exchange analysis ''')
    parser.add_option("-f", "--data", dest="dataFile", default="data.mst",
    help="File that contains stock exchange data for one company in mst format", metavar="DATAFILE")
    parser.add_option("-o", "--output", dest="outputFile",
            default="simulation.dat",
    help="""Output file. It contains visualisation data from one simulation. Data
    can be plotted using plot.sh script from tools. (Warning, output file will
    be overwriten)""", metavar="OUTFILE")
    parser.add_option("-s", "--strategy", dest="strategy",
            default="OneShotInvestor",
    help="""Investment strategy you would like to check. Currently only available
    are: OneShotInvestor, RandomInvestor, MultiShotInvestor and
    MultiShotRandomInvestor. For more information please refer to
    InvestmentStrategies.py file. If you have written your own
    strategy class in InvestmentStrategies.py filed this is the place to pass
    its name.""", metavar="DATAFILE")
    parser.add_option("-q", "--quiet",
    action="store_false", dest="verbose", default=True,
    help="don't print status messages to stdout")

    (options, _) = parser.parse_args()

    return options
    

if __name__ == "__main__":
    sys.exit(main())
