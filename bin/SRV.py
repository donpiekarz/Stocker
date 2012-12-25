"""Stocker Report Visualizer"""

from stocker.SRV.visualizer import Visualizer

if __name__ == "__main__":
    #conf = sys.argv[1]
    filename = "c:\\code\\stocker_data\\inv1.stm"

    plotter = "stocker.SRV.plotters.volume_price_plotter.VolumePricePlotter"

    Visualizer.main(filename, plotter)
