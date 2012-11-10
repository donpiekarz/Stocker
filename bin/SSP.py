

"""Stocker Stream Player"""

import os

from stocker.common.stream import Stream 

def main():
    print "hello!"
    
    cwd = os.getcwd()
    filename_in = os.path.join(cwd, '..', 'data', 'amica-2012-11-08.stm')
    
    
    stream = Stream.load(filename_in)


if __name__ == "__main__":
    main()
