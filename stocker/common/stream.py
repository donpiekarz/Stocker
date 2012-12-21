import cPickle
import csv
import datetime
import decimal
import os

from stocker.common.events import EventStreamNew, EventStockOpen, EventStockClose
from stocker.common.orders import  OrderBuy, OrderSell

class Stream:
    def __init__(self):
        self.history = []

    def next_event(self):
        for event in self.history:
            yield event

    def add_file(self, company_id, date, filename_in):
        with open(filename_in, 'r') as f:
            for row in csv.reader(f, delimiter=';'):
                #print row
                try:
                    desc = row[5]
                    if desc.startswith('TRANSAKCJA'):
                        amount = int(row[3])
                        limit_price = decimal.Decimal(row[1].replace(',', '.'))
                        timestamp = datetime.datetime.strptime("%s %s" % (date, row[0]), "%Y-%m-%d %H:%M:%S")
                        expiration_date = timestamp + datetime.timedelta(days=1)
                        self.history.append(
                            EventStreamNew(timestamp, OrderBuy(company_id, amount, limit_price, expiration_date)))
                        self.history.append(
                            EventStreamNew(timestamp, OrderSell(company_id, amount, limit_price, expiration_date)))
                except IndexError:
                    pass

    def walk(self, dir_path):
        for dir in os.walk(dir_path).next()[1]:
            for file in os.walk(os.path.join(dir_path, dir)).next()[2]:
                file_path = os.path.join(dir_path, dir, file)
                date = os.path.splitext(file)[0]
                self.add_file(dir, date, file_path)

    def add_stock_events(self):
        dates = {}

        for e in self.history:
            dates[e.timestamp.date()] = 1

        for d in dates.keys():
            self.history.append(EventStockOpen(datetime.datetime.combine(d, datetime.time(9, 0))))
            self.history.append(EventStockClose(datetime.datetime.combine(d, datetime.time(18, 0))))


    def save(self, filename_out):
        self.add_stock_events()
        self.history.sort(key=lambda event: event.timestamp)
        with open(filename_out, 'wb') as f:
            cPickle.dump(self, f, cPickle.HIGHEST_PROTOCOL)

    @staticmethod
    def load(filename_in):
        with open(filename_in, 'rU') as f:
            return cPickle.load(f)
            
