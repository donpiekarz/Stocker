
from stocker.SSP.investors.base_investor import BaseInvestor

"""
Sample XML
<Investor module="stocker.SSP.investors.reference_investor" class="ReferenceInvestor">
    <init_cash type="int">10000</init_cash>
</Investor>
"""


class ReferenceInvestor(BaseInvestor):
    init_cash = 1000

    def prepare(self):
        self.stockbroker.transfer_cash(self, self.init_cash)

    def _process_order_buy(self, event):
        if self.account.cash > event.order.limit_price:
            self._buy(event.order)
