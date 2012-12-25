import matplotlib as mpl

from stocker.SRV.plotters.base_plotter import BasePlotter
from stocker.common.events import EventInvestorReportOrderRealized
from stocker.common.orders import OrderBuy, OrderSell

class VolumePricePlotter(BasePlotter):
    def __init__(self):
        self.x_list = [] # x axis
        self.y_list = [] # y axis
        self.s_list = [] # size
        self.c_list = [] # color

    def __process_order_realized(self, event):
        x = mpl.dates.date2num(event.timestamp)
        y = event.order.limit_price
        s = event.order.amount * 10

        if isinstance(event.order, OrderBuy):
            c = 'r'
        elif isinstance(event.order, OrderSell):
            c = 'b'
        else:
            c = 'y'

        self.x_list.append(x)
        self.y_list.append(y)
        self.s_list.append(s)
        self.c_list.append(c)

    def process(self, event):
        if isinstance(event, EventInvestorReportOrderRealized):
            self.__process_order_realized(event)

    def draw_plot(self, fig):
        ax = fig.add_subplot(111)
        ax.scatter(self.x_list, self.y_list, c=self.c_list, s=self.s_list)
        ax.xaxis_date()
        ax.grid(True)

        ob = mpl.patches.Circle((0, 0), fc="r")
        os = mpl.patches.Circle((0, 0), fc="b")
        ax.legend([ob, os], ["Order Buy", "Order Sell"], loc=2)

        fig.autofmt_xdate()

