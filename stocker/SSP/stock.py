
import collections

from stocker.common.stream import Stream
from stocker.common.orders import OrderBuy, OrderSell
from stocker.common.events import EventStockOrderNew, EventStockTransaction

from stocker.SSP.stockbroker import Stockbroker


class Stock(object):
    
    stream = None
    stockbrokers = []
    companies = collections.defaultdict(dict)
    
    def __init__(self):
        pass
    
    @staticmethod
    def create_from_config(stock_tree):
        stock = Stock()
        
        stock.stream = Stream.load(stock_tree.getElementsByTagName("stream")[0].firstChild.nodeValue)
        
        for sb_tree in stock_tree.getElementsByTagName("Stockbroker"):
            sb = Stockbroker.create_from_config(stock, sb_tree)
            stock.stockbrokers.append(sb)
            
        return stock
    
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
        
        for event in self.stream.history:
            order = event.order
            order.owner = self
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
                    
                    if not buy_order.stockbroker is None:
                        event_list.append(EventStockTransaction(buy_order))
                    if not sell_order.stockbroker is None:
                        event_list.append(EventStockTransaction(sell_order))
                else:
                    break
                    
                    
        for event in event_list:
            event.order.stockbroker.process(event)
                    
            
            
            
    
    