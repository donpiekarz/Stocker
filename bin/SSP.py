

"""Stocker Stream Player"""

import sys

from stocker.SSP.player import Player

if __name__ == "__main__":
    #conf = sys.argv[1]
    conf = "ssp.xml"
    Player.main(conf)
    
