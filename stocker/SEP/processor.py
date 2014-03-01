import csv
import decimal
import os
import datetime

from stocker.common.events import EventStreamNew, EventStockOpen, EventStockClose
from stocker.common.orders import OrderBuy, OrderSell
from stocker.common.utils import Stream

class CompanyProcessor(object):
    def __init__(self, dirname, company_id):
        self.dirname = os.path.join(dirname, company_id)
        self.company_id = company_id

    def get_dates(self):
        files = [os.path.splitext(fi)[0] for fi in os.walk(self.dirname).next()[2]]
        return files

    def get_row(self, date):
        filename = os.path.join(self.dirname, date) + ".csv"

        try:
            with open(filename, 'r') as f:
                for row in reversed(list(csv.reader(f, delimiter=';'))):
                    try:
                        desc = row[5]
                        if desc.startswith('TRANSAKCJA'):
                            yield (row, self.company_id)
                    except IndexError:
                        pass

        except IOError as e:
            return


class Processor(object):
    def build_stream(self, dirname_in, filename_out):
        self.stream = Stream()
        self.stream.begin(filename_out)

        self.__process_companies(dirname_in)

        self.stream.end()

    def __process_companies(self, dirname):
        companies = []
        for company in os.walk(dirname).next()[1]:
            companies.append(CompanyProcessor(dirname, company))

        dates_set = set()
        for company in companies:
            dates_set.update(company.get_dates())

        dates_ordered = sorted(dates_set, key=lambda date: datetime.datetime.strptime(date, "%Y-%m-%d"))

        for date in dates_ordered:
            self.__process_date(date, companies)


    def __process_date(self, date, companies):
        rows = []
        correct_generators = []
        correct_day = False

        generators = [company.get_row(date) for company in companies]

        for generator in generators:
            try:
                row, company_id = generator.next()
                row = (company_id, row, generator)
                rows.append(row)
                correct_generators.append(generator)
            except StopIteration as e:
                pass

        if correct_generators:
            # correct day (have transactions)
            correct_day = True

        if correct_day:
            self.stream.add_event(EventStockOpen(
                datetime.datetime.combine(datetime.datetime.strptime(date, "%Y-%m-%d"), datetime.time(9, 0))))

        # main loop, multiplexing rows
        while correct_generators:
            row_data = min(rows, key=lambda row: datetime.datetime.strptime(row[1][0], "%H:%M:%S"))
            rows.remove(row_data)

            company_id, row, generator = row_data

            self.__process_row(row, date, company_id)

            try:
                row, company_id = generator.next()
                row = (company_id, row, generator)
                rows.append(row)
            except StopIteration as e:
                correct_generators.remove(generator)

        if correct_day:
            self.stream.add_event(EventStockClose(
                datetime.datetime.combine(datetime.datetime.strptime(date, "%Y-%m-%d"), datetime.time(18, 0))))

    def __process_row(self, row, date, company_id):
        amount = int(row[3])
        limit_price = decimal.Decimal(row[1].replace(',', '.'))
        timestamp = datetime.datetime.strptime("%s %s" % (date, row[0]), "%Y-%m-%d %H:%M:%S")
        expiration_date = timestamp + datetime.timedelta(days=1)
        self.stream.add_event(
            EventStreamNew(timestamp, OrderBuy(company_id, amount, limit_price, expiration_date)))
        self.stream.add_event(
            EventStreamNew(timestamp, OrderSell(company_id, amount, limit_price, expiration_date)))
