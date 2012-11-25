
import unittest
import tempfile
import os
import datetime

from xml.dom import minidom 

from stocker.common.stream import Stream
from stocker.common.events import EventStreamNew
from stocker.common.orders import OrderBuy, OrderSell

from stocker.SSP.stock import Stock
from stocker.SSP.stockbroker import Stockbroker
from stocker.SSP.investor import DummyInvestor, Investor


XML1 = """\
<Player>
    <Stock>
        <stream>%s</stream>
        <Stockbroker>
            <provision>0.38</provision>
            <Investor module="stocker.SSP.investor" class="DummyInvestor">
                <cash type="int">1000</cash>
            </Investor>
        </Stockbroker>
    </Stock>
    
</Player>
"""


class StockTestCase(unittest.TestCase):


    def setUp(self):
        self.stream = Stream()
        self.stream.history.append(EventStreamNew(OrderBuy("CIA", 10, 21.34, datetime.datetime.strptime("%s %s" % ("2012-11-24", "09:39:01"), "%Y-%m-%d %H:%M:%S"))))
        self.stream.history.append(EventStreamNew(OrderSell("CIA", 10, 21.34, datetime.datetime.strptime("%s %s" % ("2012-11-24", "09:39:01"), "%Y-%m-%d %H:%M:%S"))))
        
        self.stream_file = tempfile.mkstemp()[1]
        self.stream.save(self.stream_file)
        self.xml1 = XML1 % self.stream_file
        

    def tearDown(self):
        os.remove(self.stream_file)


    def _test_create_from_config(self):

        tree = minidom.parseString(self.xml1)
        stock_tree = tree.getElementsByTagName("Stock")[0]
        stock = None
        stock = Stock.create_from_config(stock_tree)
        
        self.assertIsNotNone(stock)
        self.assertIsInstance(stock.stream, Stream)
        self.assertEqual(len(stock.stream.history), 2)
        self.assertEqual(len(stock.stockbrokers), 1)
        self.assertIsNotNone(stock.stockbrokers[0])
        self.assertEqual(len(stock.stockbrokers[0].investors), 1)
        self.assertEqual(len(stock.stockbrokers[0].accounts), 1)
        self.assertEqual(stock.stockbrokers[0].stock, stock)
        self.assertIsInstance(stock.stockbrokers[0], Stockbroker)
        self.assertIsNotNone(stock.stockbrokers[0].investors[0])
        self.assertIsInstance(stock.stockbrokers[0].investors[0], DummyInvestor)
        self.assertEqual(stock.stockbrokers[0].investors[0].cash, 1000)

        
class StockbrokerTestCase(unittest.TestCase):
    class MyInvestor(Investor):
        event = None
        def process(self, event):
            self.event = event
    
    class MyStock(Stock):
        order = None
        def new_order(self, order):
            self.order = order
    
    def setUp(self):
        self.stock = self.MyStock() 
        self.stockbroker = Stockbroker(self.stock)
        self.investor = self.MyInvestor(self.stockbroker)
        self.stockbroker.add_investor(self.investor)

    def tearDown(self):
        pass

    

    def test_new_order(self):
        order1 = OrderBuy('cia', 10, 11.22, datetime.datetime.now())
        order2 = OrderSell('cia', 10, 11.33, datetime.datetime.now())
        order1.owner = self.investor
        order2.owner = self.investor
        order3 = OrderSell('cia', 10, 11.11, datetime.datetime.now())
        
        self.assertRaises(Stockbroker.MissingOwnerError, self.investor.stockbroker.new_order, order3)
        self.assertRaises(Stockbroker.NotEnoughCashError, self.investor.stockbroker.new_order, order1)
        self.assertRaises(Stockbroker.NotEnoughSharesError, self.investor.stockbroker.new_order, order2)
        
        self.stockbroker.transfer_cash(self.investor, 112.2)
        
        self.assertEqual(self.stockbroker.accounts[self.investor].cash, 112.2)
        self.assertEqual(self.stockbroker.accounts[self.investor].cash_blocked, 0)
        self.assertIsNone(self.stock.order)
        self.investor.stockbroker.new_order(order1)
        self.assertEqual(self.stockbroker.accounts[self.investor].cash, 0)
        self.assertEqual(self.stockbroker.accounts[self.investor].cash_blocked, 112.2)
        self.assertIsNotNone(self.stock.order)
        self.assertEqual(self.stock.order, order1)
        self.assertEqual(self.stock.order.owner, self.stockbroker)
        
        self.assertEqual(self.stockbroker.accounts[self.investor].shares['cia'], 0)
        self.stockbroker.accounts[self.investor].shares['cia'] += 10
        self.stock.order = None
        self.investor.stockbroker.new_order(order2)
        self.assertEqual(self.stockbroker.accounts[self.investor].shares['cia'], 0)
        self.assertEqual(self.stockbroker.accounts[self.investor].shares_blocked['cia'], 10)
        self.assertIsNotNone(self.stock.order)
        self.assertEqual(self.stock.order, order2)
        self.assertEqual(self.stock.order.owner, self.stockbroker)
        
        
        
        
        