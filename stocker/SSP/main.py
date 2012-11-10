
import os

from stocker.common.stream import Stream
from stocker.SSP.stock import Stock
from stocker.SSP.investor import DummyInvestor 

def main():
    print "hello!"
    
    data_dir = 'C:\\code\\stocker\\data'
    filename_in = os.path.join(data_dir, 'amica-2012-11-08.stm')
    
    
    stream = Stream.load(filename_in)
    stock = Stock(stream)
    
    inv1 = DummyInvestor(stock)
    
    stock.add_investor(inv1)
    
    stock.simulate()
    
    
if __name__ == "__main__":
    main()

    
    
