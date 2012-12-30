import collections
import sys
import __builtin__
from stocker.common.events import EventStockOrderNew, EventStockTransaction
from stocker.common.orders import OrderSell, OrderBuy

from stocker.common.reports import InvestorReport
from stocker.common.utils import Null

class Account(object):
    def __init__(self):
        self._total_cash = 0
        self._cash = 0
        self._cash_blocked = 0
        self._shares = collections.defaultdict(int)
        self._shares_blocked = collections.defaultdict(int)

    @property
    def cash( self ):
        return self._cash

    @property
    def cash_blocked( self ):
        return self._cash_blocked

    @property
    def shares( self ):
        return self._shares

    @property
    def shares_blocked( self ):
        return self._shares_blocked

    def add_cash(self, cash):
        self._total_cash += cash
        self._cash += cash

    def bought(self, order):
        value = order.amount * order.limit_price

        self._cash_blocked -= value
        self._shares[order.company_id] += order.amount

        assert self._cash_blocked >= 0, "Cash blocked is less then zero!"

    def sold(self, order):
        value = order.amount * order.limit_price

        self._cash += value
        self._shares_blocked[order.company_id] -= order.amount

        assert self._shares_blocked[order.company_id] >= 0, "Shares blocked (%s) is less then zero!" % order.company_id

    def block_cash(self, order):
        value = order.amount * order.limit_price

        self._cash -= value
        self._cash_blocked += value

        assert self._cash >= 0, "Cash is less then zero!"

    def block_shares(self, order):
        self._shares[order.company_id] -= order.amount
        self._shares_blocked[order.company_id] += order.amount

        assert self._shares[order.company_id] >= 0, "Shares (%s) is less then zero!" % order.company_id

    def print_summary(self):
        print "Account summary:"
        print "Total transfered cash: %.2f" % self._total_cash
        print "Current cash: %.2f" % self._cash
        print "Cash blocked: %.2f" % self._cash_blocked
        print "Shares: %s" % ["%s: %d" % (k, v) for k, v in self._shares.iteritems()]
        print "Shares blocked: %s" % ["%s: %d" % (k, v) for k, v in self._shares_blocked.iteritems()]
        print "================================================================================"


class BaseInvestor(object):
    stockbroker = None
    account = None
    report = None

    def __init__(self, stockbroker):
        self.stockbroker = stockbroker
        self.account = Account()
        self.report = Null()

    def prepare(self):
        """Prepare investor for simulation"""
        pass

    def process(self, event):
        if isinstance(event, EventStockOrderNew):
            if isinstance(event.order, OrderBuy):
                self._process_order_buy(event)
            elif isinstance(event.order, OrderSell):
                self._process_order_sell(event)

        elif isinstance(event, EventStockTransaction):
            if event.buy_order.investor == self or event.sell_order.investor == self:
                if event.buy_order.investor == self:
                    self._process_bought(event)
                elif event.sell_order.investor == self:
                    self._process_sold(event)
            else:
                self._process_transaction(event)

    @staticmethod
    def create_from_config(stockbroker, investor_tree):
        module_name = investor_tree.getAttribute("module")
        __import__(module_name)
        module = sys.modules[module_name]
        inv_class = getattr(module, investor_tree.getAttribute("class"))
        investor = inv_class(stockbroker)

        for element in investor_tree.childNodes:
            if element.nodeType == element.ELEMENT_NODE:
                element_type = getattr(__builtin__, element.getAttribute("type"))
                setattr(investor, element.nodeName, element_type(element.firstChild.nodeValue))

        if hasattr(investor, 'report_path'):
            investor.report = InvestorReport(investor.report_path)
        else:
            print "WARRING: Report file will NOT be produced (missing attribute: report_path)"

        investor.prepare()
        return investor

    def _sell(self, order):
        """Responds on buy orders"""

        if self.account.shares[order.company_id] < order.amount:
            # we dont have any shares of this company
            return

        new_order = OrderSell(order.company_id, order.amount, order.limit_price, order.expiration_date)
        self.stockbroker.new_order(new_order, self)

    def _buy(self, order):
        """Responds on sell orders"""

        if self.account.cash < order.amount * order.limit_price:
            # we dont have enough money
            return

        new_order = OrderBuy(order.company_id, order.amount, order.limit_price, order.expiration_date)
        self.stockbroker.new_order(new_order, self)

    def _process_order_buy(self, event):
        """process OrderBuy events"""
        pass

    def _process_order_sell(self, event):
        """process OrderSell events"""
        pass

    def _process_transaction(self, event):
        pass

    def _process_bought(self, event):
        pass

    def _process_sold(self, event):
        pass


class DummyInvestor(BaseInvestor):
    def process(self, event):
        print event
        pass
