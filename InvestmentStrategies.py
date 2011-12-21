from random import random

from Investor import BaseInvestor

class OneShotInvestor( BaseInvestor ):
    def __init__( self, cash = 1000, shares = 0, returnOnInvestment = 1.05 ):
        # needs to call base class constructor
        super( OneShotInvestor, self ).__init__( cash, shares )
        self.lastBuyPrice = -1
        self.roi = returnOnInvestment

    def buyingStrategy( self, price ):
        """If you don't have any shares, toss a coin and if it's heads, buy
        shares you have money for"""
        if self.cash > price and self.shares == 0:
            if self.isPriceGoindDown() : # if price is going down
                if random() > 0.5:
                    self.buy( int( self.cash / price ), price )

    def sellingStrategy( self, price ):
        """Sell all shares if you have earned more than self.roi (return on
        investment)"""
        if ( self.shares > 0 
                and ( price / self.lastBuyPrice ) > self.roi ):
                print price, self.lastBuyPrice, "Sold, earned ", price / self.lastBuyPrice
                self.sell( self.shares, price )

    def isPriceGoindDown( self ):
        if len( self.history ) > 1:
            return self.history[-2] > self.history[-1]
        return False

