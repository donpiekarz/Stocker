

import sys

from stocker.SSP.investor import Investor

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
        
        for inv_tree in stockbroker_tree.getElementsByTagName("Investor"):
            inv = Investor.create_from_config(stockbroker, inv_tree)
            
            stockbroker.investors.append(inv)
            stockbroker.accounts[inv] = Account()
        
        return stockbroker

    def new_order(self, order):
        pass
    
    def del_order(self, order):
        pass
    
    def process(self, event):
        pass
    
    pass
