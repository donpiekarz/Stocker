class Event(object):
    pass


class EventStream(Event):
    """Event in Stream"""

    def __init__(self, timestamp, order):
        self.timestamp = timestamp
        self.order = order

    def __lt__(self, other):
        return self.order < other.order

    def __repr__(self):
        return "EventStream (timestamp: %r, order: %r)" % (self.timestamp, self.order)


class EventStreamNew(EventStream):
    pass


class EventStreamDel(EventStream):
    pass


class EventStock(Event):
    """Event in Stock"""

    def __init__(self, timestamp, order):
        self.timestamp = timestamp
        self.order = order

    def __repr__(self):
        return "EventStock (timestamp: %r, order: %r)" % (self.timestamp, self.order)


class EventStockOrderNew(EventStock):
    pass


class EventStockOrderDel(EventStock):
    pass


class EventStockTransaction(Event):
    def __init__(self, timestamp, buy_order, sell_order):
        self.timestamp = timestamp
        self.buy_order = buy_order
        self.sell_order = sell_order

    def __repr__(self):
        return "EventStockTransaction (timestamp: %r, buy_order: %r, sell_order: %r)" % (
        self.timestamp, self.buy_order, self.sell_order)


class EventStockOpen(Event):
    """Now stock is open"""

    def __init__(self, timestamp):
        self.timestamp = timestamp

    def __repr__(self):
        return "EventStockOpen (timestamp: %r)" % self.timestamp


class EventStockClose(Event):
    """Now stock is close"""

    def __init__(self, timestamp):
        self.timestamp = timestamp

    def __repr__(self):
        return "EventStockClose (timestamp: %r)" % self.timestamp


class EventInvestorReportOrderPlaced(Event):
    def __init__(self, timestamp, order):
        self.timestamp = timestamp
        self.order = order

    def __repr__(self):
        return "EventInvestorReportOrderPlaced (timestamp: %r, order: %r)" % (self.timestamp, self.order)


class EventInvestorReportOrderRealized(Event):
    def __init__(self, timestamp, order):
        self.timestamp = timestamp
        self.order = order

    def __repr__(self):
        return "EventInvestorReportOrderRealized (timestamp: %r, order: %r)" % (self.timestamp, self.order)


class EventInvestorReportCashTransferred(Event):
    def __init__(self, timestamp, cash):
        self.timestamp = timestamp
        self.order = cash

    def __repr__(self):
        return "EventInvestorReportCashTransferred (timestamp: %r, order: %r)" % (self.timestamp, self.order)
