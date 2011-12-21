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

