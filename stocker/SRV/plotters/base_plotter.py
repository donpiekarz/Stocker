class BasePlotter(object):
    def process(self, event):
        raise NotImplementedError("Abstract method")

    def draw_plot(self, fig):
        raise NotImplementedError("Abstract method")

