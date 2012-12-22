import collections

from stocker.common.stream import Stream
from stocker.common.orders import OrderBuy, OrderSell
from stocker.common.events import EventStreamNew, EventStockOrderNew, EventStockTransaction, EventStockOpen, EventStockClose

from stocker.SSP.stockbroker import Stockbroker


class Stock(object):
    stream = None
    stockbrokers = []
    companies = collections.defaultdict(dict)
    stats = {}

    def __init__(self):
        self.stats['events'] = 0
        pass

    @staticmethod
    def create_from_config(stock_tree):
        stock = Stock()

        stock.stream = Stream.load(stock_tree.getElementsByTagName("stream")[0].firstChild.nodeValue)

        for sb_tree in stock_tree.getElementsByTagName("Stockbroker"):
            sb = Stockbroker.create_from_config(stock, sb_tree)
            stock.stockbrokers.append(sb)

        return stock

    def print_summary(self):
        print "Stock summary:"
        print "Proceeded events: %d" % self.stats['events']
        print "================================================================================"

    def new_order(self, order, stockbroker):
        order.stockbroker = stockbroker

        if not self.companies[order.company_id]:
            self.companies[order.company_id]['sell'] = []
            self.companies[order.company_id]['buy'] = []

        if isinstance(order, OrderBuy):
            self.companies[order.company_id]['buy'].append(order)

        elif isinstance(order, OrderSell):
            self.companies[order.company_id]['sell'].append(order)

        pass

    def del_order(self, order, stockbroker):
        order.stockbroker = stockbroker

        if not self.companies[order.company_id]:
            self.companies[order.company_id]['sell'] = []
            self.companies[order.company_id]['buy'] = []

        if isinstance(order, OrderBuy):
            self.companies[order.company_id]['buy'].remove(order)

        elif isinstance(order, OrderSell):
            self.companies[order.company_id]['sell'].remove(order)

        pass

    def simulate(self):
        for event in self.stream.next_event():
            self.stats['events'] += 1
            if isinstance(event, (EventStockOpen, EventStockClose)):
                for sb in self.stockbrokers:
                    sb.process(event)

            elif isinstance(event, (EventStreamNew, )):
                order = event.order
                order.owner = None
                self.new_order(order, None)

                for sb in self.stockbrokers:
                    sb.process(EventStockOrderNew(event.timestamp, order))

                self.match_orders()

    def match_orders(self):
        event_list = []

        for key in self.companies.keys():
            buy_list = self.companies[key]['buy']
            sell_list = self.companies[key]['sell']

            sell_list.sort(key=lambda order: order.limit_price)
            buy_list.sort(key=lambda order: order.limit_price, reverse=True)

            while len(buy_list) > 0 and len(sell_list) > 0:
                if buy_list[0].limit_price >= sell_list[0].limit_price:
                    buy_order = buy_list.pop(0)
                    sell_order = sell_list.pop(0)

                    event_list.append(EventStockTransaction(1, buy_order, sell_order))
                else:
                    break

        for event in event_list:
            if event.buy_order.stockbroker is None and event.sell_order.stockbroker is None:
                for sb in self.stockbrokers:
                    sb.process(event)
            else:
                if not event.buy_order.stockbroker is None:
                    event.buy_order.stockbroker.process(event)
                if not event.sell_order.stockbroker is None:
                    event.sell_order.stockbroker.process(event)
                    
            
            
            
    
    