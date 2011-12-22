class StockData( object ):
    def __init__( self, name, date, openPrice, highPrice, lowPrice, closePrice,
            volume ):
        self._name, self._date = str( name ), str( date )
        self._openPrice, self._highPrice, self._lowPrice, self._closePrice = float(
                openPrice ), float( highPrice ), float( lowPrice ), float(
                        closePrice )
        self._volume = float( volume )
        self._bought = 0
        self._sold = 0
    def __repr__( self ):
        """If stockData is printed, it is performed in the following format:"""
        return "%s\t%s\t%f\t%f\t%f\t%f\t%d\t%d\t%d\n" % ( self.name
                , self.date
                , self._openPrice
                , self._highPrice
                , self._lowPrice
                , self._closePrice
                , self._volume
                , self.bought
                , self.sold )

    @property
    def name( self ):
        return self._name
    @property
    def date( self ):
        return self._date
    @property
    def price( self ):
        return self._closePrice
    @property
    def volume( self ):
        return self._volume

    @property
    def bought( self ):
        return self._bought
    @bought.setter
    def bought( self, value ):
        self._bought = value
    @property
    def sold( self ):
        return self._sold
    @sold.setter
    def sold( self, value ):
        self._sold = value
