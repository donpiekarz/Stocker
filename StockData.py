class StockData( object ):
    def __init__( self, name, date, openPrice, highPrice, lowPrice, closePrice,
            volume ):
        self._name, self._date = str( name ), str( date )
        self._openPrice, self._highPrice, self._lowPrice, self._closePrice = float(
                openPrice ), float( highPrice ), float( lowPrice ), float(
                        closePrice )
        self._volume = float( volume )

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
