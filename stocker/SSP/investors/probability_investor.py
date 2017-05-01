import collections
import decimal
from collections import Counter

from stocker.SSP.investors.base_investor import BaseInvestor

"""
Sample XML

</Investor>
"""

class ProbabilityInvestor(BaseInvestor):
    init_cash = 1000
    roi = 1.05
    transaction_log_size = 500

    price = collections.defaultdict(decimal.Decimal)
    shares = collections.defaultdict(int)

    itr = 0

    transaction_log = []
    next_buy_price = 0
    next_sell_price = 1000000

    def prepare(self):
        self.stockbroker.transfer_cash(self, self.init_cash)

    def _process_order_buy(self, event):

        if event.order.limit_price <= self.next_buy_price:
            self._buy(event.order)
            self.__recalculate()

        pass

    def _process_order_sell(self, event):

        if event.order.limit_price >= self.next_sell_price:
            self._sell(event.order)
            self.__recalculate()

        pass

    def _process_bought(self, event):
        pass

    def _process_sold(self, event):
        pass

    def __get_most_common(self, l):
        data = Counter(l)
        return data.most_common(1)[0][0]

    def __get_next_buy_price(self, l):
        return self.__get_most_common(l[:self.transaction_log_size/2])

    def __get_next_sell_price(self, l):
        return self.__get_most_common(l[self.transaction_log_size/2:])

    def __recalculate(self):
        self.itr = 0
        l = sorted(self.transaction_log)
        self.next_buy_price = self.__get_next_buy_price(l)
        self.next_sell_price = self.__get_next_sell_price(l)

    def _process_transaction(self, event):

        self.transaction_log.insert(0, event.buy_order.limit_price)
        if len(self.transaction_log) > self.transaction_log_size:
            self.transaction_log.pop()

        if self.itr >= self.transaction_log_size/2:
            self.__recalculate()

        self.itr += 1

