class BaseInvestor( object ):
    """This class provides base for any Investment strategy. You should override
    two abstract methods buyingStrategy() and sellingStrategy() in order to
    implement your own investment moves"""

    def __init__( self, cash = 1000, shares = 0 ):
        self.cash = cash
        self.shares = shares
        self.history = []

    def next( self, price ):
        """Method called by the simulator on every step of the simulation"""
        self.history.append( price )

        self.sellingStrategy( price )
        self.buyingStrategy( price )

            
    def buyingStrategy( self, price ):
        """Override this method to create own investment strategy"""
        raise NotImplementedError( "Abstract method" )

    def sellingStrategy( self, price ):
        """Override this method to create own investment strategy"""
        raise NotImplementedError( "Abstract method" )

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
