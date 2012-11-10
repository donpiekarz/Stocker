
import collections

from stocker.common.orders import OrderBuy, OrderSell


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
                inv.process(event)
        
        
    
    