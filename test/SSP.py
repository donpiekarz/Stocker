
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
from stocker.SSP.investor import DummyInvestor


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
        pass


    def test_create_from_config(self):

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

        
        
        