#!/usr/bin/env python
__desc__ = """Stocker Report Visualizer"""
__additional_help__ = """Visualizes results of Stocker simulation"""

#local imports
from stocker.common import basic_program_structure
from stocker.SRV.visualizer import Visualizer


@basic_program_structure.parse_command_line(__desc__, __additional_help__)
def add_command_line_params(parser):
    """Sets up command line arguments and parses them"""
    parser.add_argument("--stream_file", help="path to simulation stream file")
    parser.add_argument("--data_visualizer", help="data visualizer",
                        default="stocker.SRV.plotters.volume_price_plotter.VolumePricePlotter")

    options = parser.parse_args()
    return options


@basic_program_structure.run_function()
def main(options):
    Visualizer.main(options.stream_file, options.data_visualizer)


if __name__ == "__main__":
    main()

