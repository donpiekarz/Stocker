class BaseInvestor( object ):
    """This class provides base for any Investment strategy. You should override
    two abstract methods buyingStrategy() and sellingStrategy() in order to
    implement your own investment moves"""

    def __init__( self, cash = 1000, shares = 0 ):
        self.cash = cash
        self.shares = shares
        self.history = []
        self.bought = 0
        self.sold = 0

    def next( self, stockData ):
        """Method called by the simulator on every step of the simulation"""
        self.history.append( stockData )
        self.bought = 0
        self.sold = 0

        self.sellingStrategy( stockData )
        self.buyingStrategy( stockData )

        stockData.bought = self.bought
        stockData.sold = self.sold
        return stockData

            
    def buyingStrategy( self, stockData ):
        """Override this method to create own investment strategy"""
        raise NotImplementedError( "Abstract method" )

    def sellingStrategy( self, stockData ):
        """Override this method to create own investment strategy"""
        raise NotImplementedError( "Abstract method" )

    def buy( self, shareCount, price ):
        self.cash -= price * shareCount
        self.shares += shareCount
        self.lastBuyPrice = price
        self.bought += shareCount
        #print "Buying at", price, " shares=", self.shares

    def sell( self, shareCount, price):
        self.cash += price * shareCount
        self.shares -= shareCount
        self.sold += shareCount
        #print "Selling at", price

    def getBalance( self ):
        return self.cash + ( self.history[-1].price * self.shares )
