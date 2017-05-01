import collections
import matplotlib as mpl

from stocker.SRV.plotters.base_plotter import BasePlotter
from stocker.common.events import EventInvestorReportOrderRealized
from stocker.common.orders import OrderBuy, OrderSell

class VolumePricePlotter(BasePlotter):
    def __init__(self):
        self.companies = {}

        self.x_list = collections.defaultdict(list) # x axis
        self.y_list = collections.defaultdict(list) # y axis
        self.s_list = collections.defaultdict(list) # size
        self.c_list = collections.defaultdict(list) # color

    def __process_order_realized(self, event):
        company = event.order.company_id
        self.companies[company] = 1

        x = mpl.dates.date2num(event.timestamp)
        y = event.order.limit_price
        s = event.order.amount * float(event.order.limit_price) / 10

        if isinstance(event.order, OrderBuy):
            c = 'r'
        elif isinstance(event.order, OrderSell):
            c = 'b'
        else:
            c = 'y'

        self.x_list[company].append(x)
        self.y_list[company].append(y)
        self.s_list[company].append(s)
        self.c_list[company].append(c)

    def process(self, event):
        if isinstance(event, EventInvestorReportOrderRealized):
            self.__process_order_realized(event)

    def draw_plot(self, fig):
        i = 1
        size = len(self.companies.keys())
        for company in self.companies.keys():
            ax = fig.add_subplot(size, 1, i)
            ax.grid(True)
            ax.set_title('Company: %s' % company)
            ax.set_xlabel("Time")
            ax.set_ylabel("Price")
            ax.scatter(self.x_list[company], self.y_list[company], c=self.c_list[company], s=self.s_list[company])
            ax.xaxis_date()

            ob = mpl.patches.Circle((0, 0), fc="r")
            os = mpl.patches.Circle((0, 0), fc="b")
            ax.legend([ob, os], ["Order Buy", "Order Sell"], loc=2)

            fig.autofmt_xdate()

            i += 1

