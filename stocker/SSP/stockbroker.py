

import sys
import collections
import decimal

from stocker.common.orders import OrderBuy, OrderSell

from stocker.SSP.investor import Investor

class Account ( object ):
    cash = 0
    cash_blocked = 0
    shares = collections.defaultdict(int)
    shares_blocked = collections.defaultdict(int)


class Stockbroker( object ):
    
    stock = None
    investors = []
    accounts = {}
    orders = {}
    
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

    def new_order(self, order, investor):
        order.investor = investor
        
        account = self.accounts[order.investor]
        
        if isinstance(order, OrderBuy):
            value = order.amount * order.limit_price
            if account.cash < value:
                raise self.NotEnoughCashError
             
            account.cash -= value
            account.cash_blocked += value
            
            self.stock.new_order(order, self)
            
        elif isinstance(order, OrderSell):
            if account.shares[order.company_id] < order.amount:
                raise self.NotEnoughSharesError
            
            account.shares[order.company_id] -= order.amount
            account.shares_blocked[order.company_id] += order.amount
            
            self.stock.new_order(order, self)
            
    
    def del_order(self, order):
        pass
    
    def process(self, event):
        for inv in self.investors:
            inv.process(event)

    def add_investor(self, investor):
        self.investors.append(investor)
        self.accounts[investor] = Account()
        
    def transfer_cash(self, owner, cash):
        self.accounts[owner].cash += cash
        
    class NotEnoughCashError(Exception):
        pass
    class NotEnoughSharesError(Exception):
        pass
        
