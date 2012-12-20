"""Stocker ETL Processor"""

import os

from stocker.common.stream import Stream

def main():
    print "hello!"

    #dirname_in = "C:\\code\\stoker_data\\small"
    #dirname_in = "C:\\code\\stoker_data\\large"
    #dirname_in = "C:\\code\\stoker_data\\amica_cia\\small"
    dirname_in = "C:\\code\\stocker_data\\small"
    filename_out = os.path.join(dirname_in, 'small.stm')

    stream = Stream()
    stream.walk(dirname_in)

    stream.save(filename_out)


if __name__ == "__main__":
    main()
