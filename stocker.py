#!/usr/bin/python
"""
Stocker is a tool for stock exchange analysis
"""

__author__ = 'Mateusz Lis'
__version__ = '0.1'

from optparse import OptionParser
from random import random
import sys
from time import time


def main(argv=None):
    global options 
    options = parseCommandLine()
    startTime = time()

    results = []
    
    for i in range( 20 ):
        inv = Investor()
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
    
class Investor( object ):

    def __init__( self, cash = 1000, shares = 0, returnOnInvestment = 1.05 ):
        self.cash = cash
        self.lastBuyPrice = -1
        self.shares = shares
        self.history = []
        self.roi = returnOnInvestment

    def next( self, price ):
        self.history.append( price )

        self.sellingStrategy( price )
        self.buyingStrategy( price )

            
    def buyingStrategy( self, price ):
        """Override this method to create own investment strategy"""
        if self.cash > price and self.shares == 0:
            #if self.isPriceGoindDown() : # if price is going down
            if random() > 0.5:
                self.buy( int( self.cash / price ), price )

    def sellingStrategy( self, price ):
        """Override this method to create own investment strategy"""
        if ( self.shares > 0 
                and ( price / self.lastBuyPrice ) > self.roi ):
                print price, self.lastBuyPrice, "Sold, earned ", price / self.lastBuyPrice
                self.sell( self.shares, price )
        pass

    def isPriceGoindDown( self ):
        if len( self.history ) > 1:
            return self.history[-2] > self.history[-1]
        return False

    def buy( self, shareCount, price ):
        self.cash -= price * shareCount
        self.shares += shareCount
        self.lastBuyPrice = price
        print "Buying at", price, " shares=", self.shares

    def sell( self, shareCount, price):
        print "Selling at", price
        self.cash += price * shareCount
        self.shares -= shareCount

    def getBalance( self ):
        return self.cash + ( self.history[-1] * self.shares )


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
