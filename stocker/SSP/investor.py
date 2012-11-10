
class Investor(object):
    def __init__(self, stock):
        self.stock = stock

class DummyInvestor(Investor):

    def process(self, event):
        pass
