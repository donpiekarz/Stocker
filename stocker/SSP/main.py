
import os

from stocker.common.stream import Stream
from stocker.SSP.stock import Stock 

def main():
    print "hello!"
    
    data_dir = 'C:\\code\\stocker\\data'
    filename_in = os.path.join(data_dir, 'amica-2012-11-08.stm')
    
    
    stream = Stream.load(filename_in)
    stock = Stock(stream)
    
    stock.simulate()
    
    
if __name__ == "__main__":
    main()

    
    
