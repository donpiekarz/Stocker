import matplotlib.pyplot as plt

from stocker.common.utils import Stream

class Visualizer(object):
    @staticmethod
    def __import_plotter(name):
        (modulename, classname) = name.rsplit('.', 1)

        mod = __import__(modulename, fromlist=[classname])
        cl = getattr(mod, classname)

        return cl

    @staticmethod
    def main(filename, plotter_str):
        plotter_class = Visualizer.__import_plotter(plotter_str)

        plotter = plotter_class()

        for event in Stream.next_event(filename):
            plotter.process(event)

        fig = plt.figure()
        plotter.draw_plot(fig)
        plt.show()



