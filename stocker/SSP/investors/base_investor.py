import collections
import sys
import __builtin__

class Account(object):
    total_cash = 0
    cash = 0
    cash_blocked = 0
    shares = collections.defaultdict(int)
    shares_blocked = collections.defaultdict(int)


class BaseInvestor(object):
    stockbroker = None
    account = None
    report = None

    def __init__(self, stockbroker):
        self.stockbroker = stockbroker
        self.account = Account()
        self.report = InvestorReport()

    def prepare(self):
        """Prepare investor for simulation"""
        pass

    def process(self, event):
        raise NotImplementedError("Abstract method")

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

        investor.prepare()
        return investor


class InvestorReport(object):
    pass


class DummyInvestor(BaseInvestor):
    def process(self, event):
        print event
        pass
