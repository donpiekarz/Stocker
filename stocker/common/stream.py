

import cPickle
import csv
import datetime
import decimal

from stocker.common.events import EventStreamNew
from stocker.common.orders import Order, OrderBuy, OrderSell

class Stream:
    
    def __init__(self):
        self.history = []
    
    def add_file(self, company_id, date, filename_in):
        with open(filename_in, 'r') as f:
            for row in csv.reader(f, delimiter=';'):
                #print row
                try:
                    desc = row[5]
                    if desc.startswith('TRANSAKCJA'):
                        amount = row[3]
                        limit_price = decimal.Decimal(row[1].replace(',', '.'))
                        timestamp = datetime.datetime.strptime("%s %s" % (date, row[0]), "%Y-%m-%d %H:%M:%S")
                        expiration_date = timestamp + datetime.timedelta(days=1)
                        self.history.append(EventStreamNew(timestamp, OrderBuy(company_id, amount, limit_price, expiration_date)))
                        self.history.append(EventStreamNew(timestamp, OrderSell(company_id, amount, limit_price, expiration_date)))
                except IndexError:
                    pass
                
        
        pass

    def save(self, filename_out):
        self.history.sort(key=lambda event: event.order.expiration_date)
        with open(filename_out, 'w') as f:
            cPickle.dump(self, f)

    @staticmethod
    def load(filename_in):
        with open(filename_in, 'r') as f:
            return cPickle.load(f)
            
