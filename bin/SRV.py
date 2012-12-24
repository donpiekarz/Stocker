"""Stocker Report Visualizer"""

from stocker.SRV.visualizer import Visualizer

if __name__ == "__main__":
    #conf = sys.argv[1]
    report1 = "c:\\code\\stocker_data\\inv1.stm"

    reports = [report1]
    Visualizer.main(reports)