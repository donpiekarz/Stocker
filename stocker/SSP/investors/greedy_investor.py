import collections
import decimal
import random

from stocker.SSP.investors.base_investor import BaseInvestor

"""
Sample XML
<Investor module="stocker.SSP.investors.greedy_investor" class="GreedyInvestor">
    <init_cash type="int">1000</init_cash>
    <buy_threshold type="float">0.6</buy_threshold>
    <roi type="float">1.06</roi>
    <report_path type="str">c:\code\stocker_data\inv1.stm</report_path>
</Investor>
"""

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
        if event.order.limit_price > self.price[company_id] * decimal.Decimal(self.roi) and self.shares[company_id]:
            self._sell(event.order)

    def _process_bought(self, event):
        company_id = event.buy_order.company_id

        self.price[company_id] = ((self.price[company_id] * self.shares[company_id]) + (
            event.buy_order.limit_price * event.buy_order.amount)) / (self.shares[company_id] + event.buy_order.amount)
        self.shares[company_id] += event.buy_order.amount

    def _process_sold(self, event):
        company_id = event.buy_order.company_id
        self.shares[company_id] -= event.sell_order.amount

        if self.shares[company_id] == 0:
            self.price[company_id] = 0


