"""Stocker ETL Processor"""

import os
from stocker.SEP.processor import Processor


def main():
    print "hello!"

    dirname_in = "C:\\code\\stocker_data\\small"
    filename_out = os.path.join(dirname_in, 'small.stm')

    processor = Processor()
    processor.build_stream(dirname_in, filename_out)

if __name__ == "__main__":
    main()
