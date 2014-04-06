#!/usr/bin/env python
__desc__ = """Stocker ETL Processor"""

__additional_help__ = """Processes input data to stream files, readable for SSP
(Stocker Stream Player)"""

#local imports
from stocker.common import basic_program_structure
from stocker.SEP.operations import available_operations


@basic_program_structure.parse_command_line(__desc__, __additional_help__)
def add_command_line_params(parser):
    """Sets up command line arguments and parses them"""

    subparsers = parser.add_subparsers(title='operations', description='available operations', help='additional help',
                                       dest="operation_tag")

    for operation in available_operations.itervalues():
        operation_parser = subparsers.add_parser(operation.tag, help=operation.help_str)
        operation.register_parser(operation_parser)

    options = parser.parse_args()
    return options


@basic_program_structure.run_function()
def main(options):
    available_operations[options.operation_tag].main(options)


if __name__ == "__main__":
    main()
