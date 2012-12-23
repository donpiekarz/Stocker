from stocker.common.events import EventInvestorReportOrderPlaced, EventInvestorReportOrderRealized, EventInvestorReportCashTransferred
from stocker.common.utils import Stream

class Report(object):
    pass


class InvestorReport(Report):
    __stream = None

    def __init__(self, filename):
        self.__stream = Stream()
        self.__stream.begin(filename)

    def order_placed(self, order):
        self.__stream.add_event(EventInvestorReportOrderPlaced(self.__now(), order))

    def order_realized(self, order):
        self.__stream.add_event(EventInvestorReportOrderRealized(self.__now(), order))

    def cash_transferred(self, cash):
        self.__stream.add_event(EventInvestorReportCashTransferred(self.__now(), cash))

    def __now(self):
        return 1

