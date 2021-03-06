import unittest
import tempfile
import datetime

from xml.dom import minidom

from stocker.common.utils import Stream
from stocker.common.events import EventStreamNew, EventStockTransaction
from stocker.common.orders import OrderBuy, OrderSell

from stocker.SSP.stock import Stock
from stocker.SSP.stockbroker import Stockbroker
from stocker.SSP.investors.base_investor import DummyInvestor, BaseInvestor


XML1 = """\
<Player>
    <Stock>
        <stream_path>%s</stream_path>
        <Stockbroker>
            <provision>0.38</provision>
            <Investor module="stocker.SSP.investors.base_investor" class="DummyInvestor">
                <cash type="int">1000</cash>
            </Investor>
        </Stockbroker>
    </Stock>
    
</Player>
"""


class StockTestCase(unittest.TestCase):
    def setUp(self):
        self.now = datetime.datetime.now()
        self.stream = Stream()

        self.stream_file = tempfile.mkstemp()[1]
        self.stream.begin(self.stream_file)
        self.stream.add_event(EventStreamNew(self.now, OrderBuy("CIA", 10, 21.34,
            datetime.datetime.strptime("%s %s" % ("2012-11-24", "09:39:01"), "%Y-%m-%d %H:%M:%S"))))
        self.stream.add_event(EventStreamNew(self.now, OrderSell("CIA", 10, 21.34,
            datetime.datetime.strptime("%s %s" % ("2012-11-24", "09:39:01"), "%Y-%m-%d %H:%M:%S"))))
        self.stream.end()

        self.xml1 = XML1 % self.stream_file


    def tearDown(self):
        #os.remove(self.stream_file)
        pass


    def test_create_from_config(self):
        tree = minidom.parseString(self.xml1)
        stock_tree = tree.getElementsByTagName("Stock")[0]
        stock = None
        stock = Stock.create_from_config(stock_tree)

        self.assertIsNotNone(stock)
        self.assertIsNotNone(stock.stream_file)
        self.assertEqual(len(stock.stockbrokers), 1)
        self.assertIsNotNone(stock.stockbrokers[0])
        self.assertEqual(len(stock.stockbrokers[0].investors), 1)
        self.assertEqual(stock.stockbrokers[0].stock, stock)
        self.assertIsInstance(stock.stockbrokers[0], Stockbroker)
        self.assertIsNotNone(stock.stockbrokers[0].investors[0])
        self.assertIsInstance(stock.stockbrokers[0].investors[0], DummyInvestor)
        self.assertEqual(stock.stockbrokers[0].investors[0].cash, 1000)


class StockbrokerTestCase(unittest.TestCase):
    class MyInvestor(BaseInvestor):
        event = None

        def process(self, event):
            self.event = event

    class MyStock(Stock):
        order = None

        def new_order(self, order, stockbroker):
            order.stockbroker = stockbroker
            self.order = order

    def setUp(self):
        self.stock = self.MyStock()
        self.stockbroker = Stockbroker(self.stock)
        self.investor = self.MyInvestor(self.stockbroker)
        self.stockbroker.add_investor(self.investor)

        self.now = datetime.datetime.now()

        self.order1 = OrderBuy('cia', 10, 11.22, self.now)
        self.order2 = OrderSell('cia', 10, 11.33, self.now)

    def tearDown(self):
        pass


    def test_new_order(self):
        self.assertRaises(Stockbroker.NotEnoughCashError, self.investor.stockbroker.new_order, self.order1,
            self.investor)
        self.assertRaises(Stockbroker.NotEnoughSharesError, self.investor.stockbroker.new_order, self.order2,
            self.investor)

        self.stockbroker.transfer_cash(self.investor, 112.2)

        self.assertEqual(self.investor.account.cash, 112.2)
        self.assertEqual(self.investor.account.cash_blocked, 0)
        self.assertIsNone(self.stock.order)
        self.investor.stockbroker.new_order(self.order1, self.investor)
        self.assertEqual(self.investor.account.cash, 0)
        self.assertEqual(self.investor.account.cash_blocked, 112.2)
        self.assertIsNotNone(self.stock.order)
        self.assertEqual(self.stock.order, self.order1)
        self.assertEqual(self.stock.order.investor, self.investor)
        self.assertEqual(self.stock.order.stockbroker, self.stockbroker)

        self.assertEqual(self.investor.account.shares['cia'], 0)
        self.investor.account.shares['cia'] += 10
        self.stock.order = None
        self.investor.stockbroker.new_order(self.order2, self.investor)
        self.assertEqual(self.investor.account.shares['cia'], 0)
        self.assertEqual(self.investor.account.shares_blocked['cia'], 10)
        self.assertIsNotNone(self.stock.order)
        self.assertEqual(self.stock.order, self.order2)
        self.assertEqual(self.stock.order.investor, self.investor)
        self.assertEqual(self.stock.order.stockbroker, self.stockbroker)

    def test_process_transaction(self):
        self.investor.account.cash = 0
        self.investor.account.cash_blocked = 0
        self.investor.account.shares['cia'] = 0
        self.investor.account.shares_blocked['cia'] = 0

        self.stockbroker.transfer_cash(self.investor, 112.2)
        self.investor.stockbroker.new_order(self.order1, self.investor)

        self.assertEqual(self.investor.account.cash, 0)
        self.assertEqual(self.investor.account.cash_blocked, 112.2)
        self.assertEqual(self.investor.account.shares['cia'], 0)
        self.assertEqual(self.investor.account.shares_blocked['cia'], 0)
        event = EventStockTransaction(self.now, self.order1, None)
        self.stockbroker.process(event)
        self.assertEqual(self.investor.account.cash, 0)
        self.assertEqual(self.investor.account.cash_blocked, 0)
        self.assertEqual(self.investor.account.shares['cia'], 10)
        self.assertEqual(self.investor.account.shares_blocked['cia'], 0)
        self.assertEqual(self.investor.event, event)

        self.investor.stockbroker.new_order(self.order2, self.investor)
        self.assertEqual(self.investor.account.cash, 0)
        self.assertEqual(self.investor.account.cash_blocked, 0)
        self.assertEqual(self.investor.account.shares['cia'], 0)
        self.assertEqual(self.investor.account.shares_blocked['cia'], 10)
        event = EventStockTransaction(self.now, None, self.order2)
        self.stockbroker.process(event)
        self.assertEqual(self.investor.account.cash, 113.3)
        self.assertEqual(self.investor.account.cash_blocked, 0)
        self.assertEqual(self.investor.account.shares['cia'], 0)
        self.assertEqual(self.investor.account.shares_blocked['cia'], 0)
        self.assertEqual(self.investor.event, event)
        
        
        
        
        
        