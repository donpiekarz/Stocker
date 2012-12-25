import matplotlib.pyplot as plt

from stocker.SRV.plotters.volume_price_plotter import VolumePricePlotter
from stocker.common.utils import Stream

class Visualizer(object):
    @staticmethod
    def main(reports):
        report = reports[0]

        plotter = VolumePricePlotter()

        for event in Stream.next_event(report):
            plotter.process(event)

        fig = plt.figure()

        plotter.draw_plot(fig)

        plt.show()



