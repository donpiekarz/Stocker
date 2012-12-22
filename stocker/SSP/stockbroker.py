from stocker.common.orders import OrderBuy, OrderSell
from stocker.common.events import EventStockTransaction

from stocker.SSP.investors.base_investor import BaseInvestor

class Stockbroker(object):
    stock = None
    investors = []

    def __init__(self, stock):
        self.stock = stock

    @staticmethod
    def create_from_config(stock, stockbroker_tree):
        stockbroker = Stockbroker(stock)

        for inv_tree in stockbroker_tree.getElementsByTagName("Investor"):
            inv = BaseInvestor.create_from_config(stockbroker, inv_tree)
            stockbroker.investors.append(inv)

        return stockbroker

    def new_order(self, order, investor):
        order.investor = investor

        account = order.investor.account

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
        if isinstance(event, EventStockTransaction):
            if hasattr(event.buy_order, 'investor') or hasattr(event.sell_order, 'investor'): self.process_transaction(
                event)
            else:
                for inv in self.investors:
                    inv.process(event)

        else:
            for inv in self.investors:
                inv.process(event)

    def process_transaction(self, event):
        if hasattr(event.buy_order, 'investor') and event.buy_order.investor:
            order = event.buy_order
        elif hasattr(event.sell_order, 'investor') and event.sell_order.investor:
            order = event.sell_order
        else:
            return

        account = order.investor.account
        value = order.amount * order.limit_price

        if isinstance(order, OrderBuy):
            account.cash_blocked -= value
            account.shares[order.company_id] += order.amount

        elif isinstance(order, OrderSell):
            account.cash += value
            account.shares_blocked[order.company_id] -= order.amount

        order.investor.process(event)


    def add_investor(self, investor):
        self.investors.append(investor)

    def transfer_cash(self, owner, cash):
        owner.account.total_cash += cash
        owner.account.cash += cash

    class NotEnoughCashError(Exception):
        pass

    class NotEnoughSharesError(Exception):
        pass
        
