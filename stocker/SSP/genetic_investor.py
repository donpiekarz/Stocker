
from stocker.common.events import EventStockOpen, EventStockClose, EventStockTransaction
from stocker.SSP.investor import Investor

class GA( object ):
    def __init__(self, min_price_list, max_price_list, last_price_list, volume_list):
        self.min_price_list = min_price_list
        self.max_price_list = max_price_list
        self.last_price_list = last_price_list
        self.volume_list = volume_list
        

class GeneticInvestor( Investor ):
    learning = 0
    cash = 0
    
    min_price_list = []
    max_price_list = []
    last_price_list = []
    volume_list = []
    
    ga = None
    days = 0
    
    def process(self, event):
        #print event
        if isinstance(event, EventStockOpen):
            self.days += 1
            self.volume = 0
            self.last_price = None
            self.min_price = 10000
            self.max_price = 0
            if self.learning <= self.days:
                self.ga = GA(self.min_price_list, self.max_price_list, self.last_price_list, self.volume_list)
                
        elif isinstance(event, EventStockClose):
            self.min_price_list.append(self.min_price)
            self.max_price_list.append(self.max_price)
            self.last_price_list.append(self.last_price)
            self.volume_list.append(self.volume)
            
        elif isinstance(event, EventStockTransaction):
            self.volume += event.buy_order.amount
            self.last_price = event.buy_order.limit_price
            if self.max_price < event.buy_order.limit_price: self.max_price = event.buy_order.limit_price
            if self.min_price > event.buy_order.limit_price: self.min_price = event.buy_order.limit_price
            
                
            
        