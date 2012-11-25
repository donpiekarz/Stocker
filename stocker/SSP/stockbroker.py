

import sys

from stocker.SSP.investor import Investor

class Account ( object ):
    cash = 0
    cash_blocked = 0
    shares = []
    shares_blocked = []

    class NotEnoughCashError(Exception):
        pass
    class NotEnoughSharesError(Exception):
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
        for inv in self.investors:
            inv.process(event)

    def add_investor(self, investor):
        self.investors.append(investor)
        self.accounts[investor] = Account()
        
    def transfer_cash(self, owner, amount):
        pass
        
    class MissingOwnerError(Exception):
        pass
        
