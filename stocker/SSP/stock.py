
import collections

from stocker.common.orders import OrderBuy, OrderSell
from stocker.common.events import EventStockOrderNew, EventStockTransaction


class Stock(object):
    
    def __init__(self, stream):
        self.stream = stream
        self.investors = []
        self.companies = collections.defaultdict(dict)
        
    def add_investor(self, investor):
        self.investors.append(investor)
    
    def new_order(self, order):
        if order.owner is None:
            raise Exception("Order.owner is None!")

        if not self.companies[order.company_id]:
            self.companies[order.company_id]['sell'] = []
            self.companies[order.company_id]['buy'] = []
        
        if isinstance(order, OrderBuy):
            self.companies[order.company_id]['buy'].append(order)
            
        elif isinstance(order, OrderSell):
            self.companies[order.company_id]['sell'].append(order)
        
        pass
    
    def del_order(self, order):
        if order.owner is None:
            raise Exception("Order.owner is None!")
        
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
            self.new_order(order)
            
            for inv in self.investors:
                inv.process(EventStockOrderNew(order))
                
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
                    
                    if buy_order.owner != self:
                        event_list.append(EventStockTransaction(buy_order))
                    if sell_order.owner != self:
                        event_list.append(EventStockTransaction(sell_order))
                else:
                    break
                    
                    
        for event in event_list:
            event.order.owner.process(event)
                    
            
            
            
    
    