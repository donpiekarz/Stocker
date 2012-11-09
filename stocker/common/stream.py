

import cPickle
import csv

#from common.events import EventStream
from stocker.common.orders import OrderBuy, OrderSell

class Stream:
    
    def __init__(self):
        self.history = []
    
    def add_file(self, company_id, date, filename_in):
        with open(filename_in, 'r') as f:
            for row in csv.reader(f, delimiter=';'):
                print row
                try:
                    desc = row[5]
                    if desc.startswith('TRANSAKCJA'):
                        amount = row[3]
                        limit_price = row[1]
                        expiration_date = row[0] 
                        self.history.append(OrderBuy(company_id, amount, limit_price, expiration_date))
                        self.history.append(OrderSell(company_id, amount, limit_price, expiration_date))
                except:
                    pass
                
        
        pass

    def save(self, filename_out):
        with open(filename_out, 'w') as f:
            cPickle.dump(self, f)
            
