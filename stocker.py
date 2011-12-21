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
from InvestmentStrategies import OneShotInvestor

def main(argv=None):
    global options 
    options = parseCommandLine()
    startTime = time()

    results = []
    
    for i in range( 20 ):
        inv = OneShotInvestor()
        start = 850
        end = -1
        with open( options.dataFile ) as dataFile:
            data = dataFile.readlines()
            name, date, openPrice, highPrice, lowPrice, firstClosePrice, vol = data[start].split( "," )
            name, date, openPrice, highPrice, lowPrice, lastClosePrice, vol = data[end].split( "," )
            firstClosePrice, lastClosePrice = float( firstClosePrice ), float( lastClosePrice )
            for line in data[ start:end ]:
                if line[0] == "<":
                    continue
                name, date, openPrice, highPrice, lowPrice, closePrice, vol = line.split( "," )
                #print date, closePrice
                inv.next( float( closePrice ) )
            results.append( inv.getBalance() )
            

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
    parser.add_option("-q", "--quiet",
    action="store_false", dest="verbose", default=True,
    help="don't print status messages to stdout")

    (options, _) = parser.parse_args()

    return options
    

if __name__ == "__main__":
    sys.exit(main())
