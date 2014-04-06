#!/usr/bin/env python
__desc__ = """Stocker Stream Player"""
__additional_help__ = """Performs Stocker simulations"""

#local imports
from stocker.common import basic_program_structure
from stocker.SSP.player import Player


@basic_program_structure.parse_command_line(__desc__, __additional_help__)
def add_command_line_params(parser):
    """Sets up command line arguments and parses them"""
    parser.add_argument("conf_file", help="path to simulation configuration file")
    options = parser.parse_args()
    return options


@basic_program_structure.run_function()
def main(options):
    Player.main(options.conf_file)


if __name__ == "__main__":
    main()
