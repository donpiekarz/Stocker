from xml.dom import minidom
import datetime

from stocker.SSP.stock import Stock

class Player(object):
    @staticmethod
    def main(config_file):
        print "hello!"

        main_tree = minidom.parse(config_file)

        stock_tree = main_tree.childNodes[0].getElementsByTagName("Stock")[0]
        stock = Stock.create_from_config(stock_tree)

        start_time = datetime.datetime.now()
        stock.simulate()
        stop_time = datetime.datetime.now()

        # summary
        print "End of simulation!"
        print "Simulation lasted: %s" % (stop_time - start_time)


if __name__ == "__main__":
    conf = "ssp.xml"
    Player.main(conf)

    
    
