import sys
import __builtin__

class BaseInvestor(object):
    stockbroker = None

    def __init__(self, stockbroker, account):
        self.stockbroker = stockbroker
        self.account = account

    def prepare(self):
        """Prepare investor to simulation"""
        pass

    def process(self, event):
        raise NotImplementedError("Abstract method")

    @staticmethod
    def create_from_config(stockbroker, account, investor_tree):
        module_name = investor_tree.getAttribute("module")
        __import__(module_name)
        module = sys.modules[module_name]
        inv_class = getattr(module, investor_tree.getAttribute("class"))
        investor = inv_class(stockbroker, account)

        for element in investor_tree.childNodes:
            if element.nodeType == element.ELEMENT_NODE:
                element_type = getattr(__builtin__, element.getAttribute("type"))
                setattr(investor, element.nodeName, element_type(element.firstChild.nodeValue))

        investor.prepare()
        return investor


class DummyInvestor(BaseInvestor):
    def process(self, event):
        print event
        pass
