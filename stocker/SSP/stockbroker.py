from stocker.common.orders import OrderBuy, OrderSell
from stocker.common.events import EventStockTransaction

from stocker.SSP.investors.base_investor import BaseInvestor

class Stockbroker(object):
    stock = None
    investors = []
    stats = {}

    def __init__(self, stock):
        self.stock = stock

        self.stats['orders'] = 0

    @staticmethod
    def create_from_config(stock, stockbroker_tree):
        stockbroker = Stockbroker(stock)

        for inv_tree in stockbroker_tree.getElementsByTagName("Investor"):
            inv = BaseInvestor.create_from_config(stockbroker, inv_tree)
            stockbroker.investors.append(inv)

        return stockbroker

    def print_summary(self):
        print "Stockbroker summary:"
        print "Placed orders: %d" % self.stats['orders']
        print "================================================================================"

        for inv in self.investors:
            print "%r" % inv
            inv.account.print_summary()

    def new_order(self, order, investor):
        self.stats['orders'] += 1
        order.investor = investor

        account = order.investor.account

        if isinstance(order, OrderBuy):
            value = order.amount * order.limit_price
            if account.cash < value:
                raise self.NotEnoughCashError

            account.block_cash(order)

            self.stock.new_order(order, self)
            investor.report.order_placed(order)

        elif isinstance(order, OrderSell):
            if account.shares[order.company_id] < order.amount:
                raise self.NotEnoughSharesError

            account.block_shares(order)

            self.stock.new_order(order, self)
            investor.report.order_placed(order)


    def del_order(self, order):
        pass

    def process(self, event):
        if isinstance(event, EventStockTransaction):
            if event.buy_order.investor or event.sell_order.investor:
                self.process_transaction(event)
            else:
                for inv in self.investors:
                    inv.process(event)

        else:
            for inv in self.investors:
                inv.process(event)

    def process_transaction(self, event):
        if event.buy_order.investor:
            self.__process_transaction_buy(event)

        if event.sell_order.investor:
            self.__process_transaction_sell(event)

    def __process_transaction_buy(self, event):
        order = event.buy_order
        order.investor.report.order_realized(order)

        order.investor.account.bought(order)

        order.investor.process(event)

    def __process_transaction_sell(self, event):
        order = event.sell_order
        order.investor.report.order_realized(order)

        order.investor.account.sold(order)

        order.investor.process(event)

    def add_investor(self, investor):
        self.investors.append(investor)

    def transfer_cash(self, owner, cash):
        owner.account.add_cash(cash)
        owner.report.cash_transferred(cash)

    class NotEnoughCashError(Exception):
        pass

    class NotEnoughSharesError(Exception):
        pass
        
