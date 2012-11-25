

import sys

class Account ( object ):
    pass


class Stockbroker( object ):
    
    stock = None
    investors = []
    accounts = {}
    
    def __init__(self, stock):
        self.stock = stock

    @staticmethod
    def create_from_config(stock, stockbroker_tree):
        stockbroker = Stockbroker(stock)
        
        return stockbroker

    def load_config(self, stockbroker_tree):
        for inv_tree in stockbroker_tree.getElementsByTagName("Investor"):
            module_name = inv_tree.getAttribute("module")
            __import__(module_name)
            module = sys.modules[module_name]
            
            inv_class = getattr(module, inv_tree.getAttribute("class"))
            
            inv = inv_class(self, inv_tree)
            
            self.investors.append(inv)
            self.accounts[inv] = Account()

    def new_order(self, order):
        pass
    
    def del_order(self, order):
        pass
    
    def process(self, event):
        pass
    
    pass
