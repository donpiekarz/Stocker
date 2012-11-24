
import os
import sys
from xml.dom import minidom 

from stocker.SSP.stock import Stock
from stocker.SSP.investor import DummyInvestor 

class Player ( object ):
    
    @staticmethod
    def main(config_file):
        print "hello!"
        
        main_tree = minidom.parse(config_file)
        
        stock_tree = main_tree.childNodes[0].getElementsByTagName("Stock")[0]
        stock = Stock(stock_tree)
        
        """
        data_dir = 'C:\\code\\stocker\\data'
        filename_in = os.path.join(data_dir, 'amica-2012-11-08.stm')
        
        
        stream = Stream.load(filename_in)
        
        
        inv1 = DummyInvestor(stock)
        
        stock.add_investor(inv1)
        """
        
        stock.simulate()
    
    
if __name__ == "__main__":
    conf = "ssp.xml"
    Player.main(conf)

    
    
