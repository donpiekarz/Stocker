from stocker.common.events import Event
from stocker.common.utils import Stream

class Report(object):
    pass


class InvestorReport(Report):
    __stream = None

    def __init__(self, filename):
        self.__stream = Stream()
        self.__stream.begin(filename)

    def order_placed(self, order):
        self.__stream.add_event(InvestorReport.OrderPlaced(self.__now(), order))

    def order_realized(self, order):
        self.__stream.add_event(InvestorReport.OrderRealized(self.__now(), order))

    def cash_transferred(self, cash):
        self.__stream.add_event(InvestorReport.CashTransferred(self.__now(), cash))

    def __now(self):
        return 1

    class OrderPlaced(Event):
        def __init__(self, timestamp, order):
            self.timestamp = timestamp
            self.order = order

    class OrderRealized(Event):
        def __init__(self, timestamp, order):
            self.timestamp = timestamp
            self.order = order

    class CashTransferred(Event):
        def __init__(self, timestamp, cash):
            self.timestamp = timestamp
            self.order = cash


