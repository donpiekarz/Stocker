

"""Stocker ETL Processor"""

import os

from stocker.common.stream import Stream 

def main():
    print "hello!"
    
    dirname_in = "C:\\code\\stoker_data"
    filename_out = os.path.join(dirname_in, 'stream1.stm')
    
    stream = Stream()
    stream.walk(dirname_in)
    
    stream.save(filename_out)


if __name__ == "__main__":
    main()
