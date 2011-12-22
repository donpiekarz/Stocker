from random import random

from Investor import BaseInvestor

class OneShotInvestor( BaseInvestor ):
    def __init__( self, cash = 1000, shares = 0, returnOnInvestment = 1.05 ):
        # needs to call base class constructor
        super( OneShotInvestor, self ).__init__( cash, shares )
        self.lastBuyPrice = -1
        self.roi = returnOnInvestment

    def buyingStrategy( self, stockData ):
        """If you don't have any shares, toss a coin and if it's heads, buy
        shares you have money for"""
        price = stockData.price
        if self.cash > price and self.shares == 0:
            if self.isPriceGoindDown() : # if price is going down
                if random() > 0.5:
                    self.buy( int( self.cash / price ), price )

    def sellingStrategy( self, stockData ):
        """Sell all shares if you have earned more than self.roi (return on
        investment)"""
        price = stockData.price
        if ( self.shares > 0 
                and ( price / self.lastBuyPrice ) > self.roi ):
                self.sell( self.shares, price )

    def isPriceGoindDown( self ):
        if len( self.history ) > 1:
            return self.history[-2].price > self.history[-1].price
        return False

class RandomInvestor( BaseInvestor ):
    def __init__( self, cash = 1000, shares = 0 ):
        # needs to call base class constructor
        super( RandomInvestor, self ).__init__( cash, shares )

    def buyingStrategy( self, stockData ):
        """If you don't have any shares, toss a coin and if it's heads, buy
        shares you have money for"""
        price = stockData.price
        if self.cash > price and self.shares == 0 and random() > 0.5:
            self.buy( int( self.cash / price ), price )

    def sellingStrategy( self, stockData ):
        """If you have any shares, toss a coin and if it's heads, sell all of
        them"""
        price = stockData.price
        if ( self.shares > 0 
                and random() > 0.5 ):
                self.sell( self.shares, price )

class MultiShotInvestor( BaseInvestor ):
    """Base concept for this investor is the following:
    - when it goes down, buy small packages of shares
    - when it goes up, sell with more than given roi (return on investment)"""
    def __init__( self, cash = 1000, shares = 0, packSize = 100, roi = 1.05 ):
        # needs to call base class constructor
        super( MultiShotInvestor, self ).__init__( cash, shares )

        self.packagePrices = []
        self.packageShareCounts = []
        self.packSize = packSize
        self.roi = roi

    def buyingStrategy( self, stockData ):
        price = stockData.price
        if self.isPriceGoingDown() and self.cash > self.packSize:
            if random() > 0.2:
                if self.packSize / price:
                    sharesToBuy = int( self.packSize / price )
                    self.buy( sharesToBuy, price )
                    self.packagePrices.append( price )
                    self.packageShareCounts.append( sharesToBuy )
    
    def sellingStrategy( self, stockData):
        price = stockData.price
        for buyPriceInd in range( len( self.packagePrices ) ):
            buyPrice = self.packagePrices[buyPriceInd] 
            if price / buyPrice > self.roi:
                if random() > 0.5:
                    self.sell( self.packageShareCounts[ buyPriceInd ], price )
                    del self.packagePrices[buyPriceInd]
                    del self.packageShareCounts[buyPriceInd]
                    break
    def isPriceGoingDown( self ):
        if len( self.history ) > 10:
            return ( self.history[-11].price / self.history[-1].price ) > self.roi
        return False
