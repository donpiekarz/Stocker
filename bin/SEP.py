

"""Stocker ETL Processor"""

import os

from stocker.common.stream import Stream 

def main():
    print "hello!"
    
    cwd = os.getcwd()
    filename_in = os.path.join(cwd, '..', 'data', 'amica-2012-11-08.csv')
    filename_out = os.path.join(cwd, '..', 'data', 'amica-2012-11-08.stm')
    
    company_id = 'amica'
    date = '2012-11-08'
    
    stream = Stream()
    stream.add_file(company_id, date, filename_in)
    
    stream.save(filename_out)


if __name__ == "__main__":
    main()
