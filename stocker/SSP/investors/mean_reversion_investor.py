import collections
import decimal
import random

from stocker.SSP.investors.base_investor import BaseInvestor

"""
Sample XML
<Investor module="stocker.SSP.investors.mean_reversion_investor" class="MeanReversionInvestor">
    <init_cash type="int">1000</init_cash>
    <buy_threshold type="float">0.6</buy_threshold>
    <roi type="float">1.06</roi>
    <report_path type="str">c:\code\stocker_data\inv1.stm</report_path>
</Investor>
"""

class MeanReversionInvestor(BaseInvestor):
    init_cash = 1000
    buy_threshold = 0.5
    buy_mean_deviation = decimal.Decimal(-0.006)
    sell_mean_deviation = decimal.Decimal(0.004)
    mean = None
    history_price = []
    history_amount = []
    size = 100

    def prepare(self):
        self.stockbroker.transfer_cash(self, self.init_cash)

    def _process_order_buy(self, event):
        if self.mean is not None and self.mean + self.mean * self.buy_mean_deviation > event.order.limit_price:
            self._buy(event.order)

    def _process_order_sell(self, event):
        #print self.count, self.mean
        if self.mean is not None and self.mean + self.mean * self.sell_mean_deviation < event.order.limit_price:
            self._sell(event.order)

    def _process_bought(self, event):
        company_id = event.buy_order.company_id

    def _process_sold(self, event):
        pass

    def _process_transaction(self, event):
        self.history_price.append(event.buy_order.limit_price * event.buy_order.amount)
        self.history_amount.append(event.buy_order.amount)
        if len(self.history_price) >= self.size:
            self.history_price.pop(0)
            self.history_amount.pop(0)
            self.mean = decimal.Decimal(sum(self.history_price) / sum(self.history_amount))
