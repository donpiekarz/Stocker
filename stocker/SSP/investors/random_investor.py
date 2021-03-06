import random

from stocker.SSP.investors.base_investor import BaseInvestor
from stocker.common.events import EventStockOrderNew, EventStockTransaction
from stocker.common.orders import OrderBuy, OrderSell

"""
Sample XML
<Investor module="stocker.SSP.investors.random_investor" class="RandomInvestor">
    <init_cash type="int">1000</init_cash>
    <buy_threshold type="float">0.6</buy_threshold>
    <sell_threshold type="float">0.6</sell_threshold>
    <report_path type="str">c:\code\stocker_data\inv1.stm</report_path>
</Investor>
"""

class RandomInvestor(BaseInvestor):
    init_cash = 1000
    buy_threshold = 0.5
    sell_threshold = 0.5

    def prepare(self):
        self.stockbroker.transfer_cash(self, self.init_cash)

    def process(self, event):
        if isinstance(event, EventStockOrderNew):
            order = event.order
            if isinstance(order, OrderBuy) and random.random() > self.sell_threshold: self.__process_buy_order(order)
            elif isinstance(order, OrderSell) and random.random() > self.buy_threshold: self.__process_sell_order(order)

        elif isinstance(event, EventStockTransaction):
            if hasattr(event.buy_order, 'investor') and event.buy_order.investor == self:
                #print "bought!", event.buy_order
                pass

            elif hasattr(event.sell_order, 'investor') and event.sell_order.investor == self:
                #print "sold!", event.sell_order
                pass

    def __process_buy_order(self, order):
        """Responds on buy orders"""

        if not self.account.shares[order.company_id] > order.amount:
            # we dont have any shares of this company
            return

        new_order = OrderSell(order.company_id, order.amount, order.limit_price, order.expiration_date)
        self.stockbroker.new_order(new_order, self)

    def __process_sell_order(self, order):
        """Responds on sell orders"""

        if self.account.cash < order.amount * order.limit_price:
            # we dont have enough money
            return

        new_order = OrderBuy(order.company_id, order.amount, order.limit_price, order.expiration_date)
        self.stockbroker.new_order(new_order, self)



