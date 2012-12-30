import collections
import decimal
import random

from stocker.SSP.investors.base_investor import BaseInvestor

class GreedyInvestor(BaseInvestor):
    init_cash = 1000
    buy_threshold = 0.5
    roi = 1.05

    price = collections.defaultdict(decimal.Decimal)
    shares = collections.defaultdict(int)

    def prepare(self):
        self.stockbroker.transfer_cash(self, self.init_cash)

    def _process_order_buy(self, event):
        if random.random() > self.buy_threshold:
            self._buy(event.order)

    def _process_order_sell(self, event):
        company_id = event.order.company_id
        if event.order.limit_price > self.price[company_id] and self.shares[company_id]:
            self._sell(event.order)

    def _process_bought(self, event):
        company_id = event.buy_order.company_id

        self.price[company_id] = ((self.price[company_id] * self.shares[company_id]) + (
        event.buy_order.limit_price * event.buy_order.amount)) / (self.shares[company_id] + event.buy_order.amount)
        self.shares[company_id] += event.buy_order.amount

    def _process_sold(self, event):
        company_id = event.buy_order.company_id
        self.shares[company_id] -= event.sell_order.amount


