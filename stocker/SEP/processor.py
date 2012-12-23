import csv
import decimal
import os
import datetime

from stocker.common.events import EventStreamNew, EventStockOpen, EventStockClose
from stocker.common.orders import OrderBuy, OrderSell
from stocker.common.stream import Stream

class Processor(object):
    def build_stream(self, dirname_in, filename_out):
        self.stream = Stream()
        self.stream.begin(filename_out)

        self.__walk(dirname_in)

        self.stream.end()


    def __walk(self, dir_path):
        for dir in os.walk(dir_path).next()[1]:
            files = [file for file in os.walk(os.path.join(dir_path, dir)).next()[2]]

            # order files by date
            files.sort(key=lambda file: datetime.datetime.strptime(os.path.splitext(file)[0], "%Y-%m-%d"))

            for file in files:
                file_path = os.path.join(dir_path, dir, file)
                date = os.path.splitext(file)[0]
                self.__process_file(dir, date, file_path)

    def __process_file(self, company_id, date, filename_in):
        self.stream.add_event(EventStockOpen(
            datetime.datetime.combine(datetime.datetime.strptime(date, "%Y-%m-%d"), datetime.time(9, 0))))

        with open(filename_in, 'r') as f:
            for row in reversed(list(csv.reader(f, delimiter=';'))):
                #print row
                try:
                    desc = row[5]
                    if desc.startswith('TRANSAKCJA'):
                        amount = int(row[3])
                        limit_price = decimal.Decimal(row[1].replace(',', '.'))
                        timestamp = datetime.datetime.strptime("%s %s" % (date, row[0]), "%Y-%m-%d %H:%M:%S")
                        expiration_date = timestamp + datetime.timedelta(days=1)
                        self.stream.add_event(
                            EventStreamNew(timestamp, OrderBuy(company_id, amount, limit_price, expiration_date)))
                        self.stream.add_event(
                            EventStreamNew(timestamp, OrderSell(company_id, amount, limit_price, expiration_date)))
                except IndexError:
                    pass

        self.stream.add_event(EventStockClose(
            datetime.datetime.combine(datetime.datetime.strptime(date, "%Y-%m-%d"), datetime.time(18, 0))))
