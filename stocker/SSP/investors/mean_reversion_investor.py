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
    buy_mean_deviation = 0.05
    sell_mean_deviation = 0.05
    mean = 0.0
    flag = False

    def prepare(self):
        self.stockbroker.transfer_cash(self, self.init_cash)

    def _process_order_buy(self, event):
        if self.flag == False:
            self._buy(event.order)
            self.flag = True
        pass

    def _process_order_sell(self, event):
        company_id = event.order.company_id
        #self._sell(event.order)

    def _process_bought(self, event):
        company_id = event.buy_order.company_id
        print "kupilem!!!!!!!!!"

    def _process_sold(self, event):
        pass

    def _process_transaction(self, event):
        pass

