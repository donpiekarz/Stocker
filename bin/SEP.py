#!/usr/bin/env python
__desc__ = """Stocker ETL Processor"""

__additional_help__ = """Processes input data to stream files, readable for SSP
(Stocker Stream Player)"""

import os

#local imports
from stocker.common import basic_program_structure
from stocker.SEP.processor import Processor

@basic_program_structure.parse_command_line(__desc__, __additional_help__)
def add_command_line_params(parser):
    """Sets up command line arguments and parses them"""
    # parser.add_argument("data_path", help="path original data")
    # parser.add_argument("output_stream_file", help="path to stream file")
    options = parser.parse_args()
    return options

@basic_program_structure.run_function()
def main(options):

    # dirname_in = options.data_path
    # filename_out = options.output_stream_file
    #
    # processor = Processor()
    # processor.build_stream(dirname_in, filename_out)

    print("hello")

    import stocker.SEP.operations

    print(stocker.SEP.operations.all_operations)



if __name__ == "__main__":
    main()
