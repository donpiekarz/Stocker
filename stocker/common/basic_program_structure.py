import argparse
import traceback
import time

#local imports
from stocker.common.version import stocker_version


def create_parser(desc, additional_help):
    """Common command line parser for every Stocker executable"""
    parser = argparse.ArgumentParser(description="%s, version: %s\n%s"\
            % (desc, stocker_version, additional_help) \
            , formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("-v", "--verbose", help="increase output verbosity",
                            action="store_true")
    parser.add_argument("-t", "--measure_time", help="display time of execution",
                            action="store_true")
    return parser

def parse_command_line(desc, additional_help):
    def call_parse(parse_fun):
        def inner_call_parse():
            return parse_fun(create_parser(desc, additional_help))

        global command_line_parser
        command_line_parser = inner_call_parse
        return inner_call_parse
    return call_parse

def basic_parser():
    options = create_parser("Part of Stocker distribution", "").parse_args()
command_line_parser = basic_parser

def run_function():
    def run_program(main):
        """Basic program routine decorator"""
        def inner_run_program():
            start_time = time.time()
            options = command_line_parser()
            try:
                main(options)
            except:
                print "An error occured during execution"
                traceback.print_exc()

            if options.measure_time:
                print "Execution time: %s" % (time.time() - start_time)
        return inner_run_program
    return run_program

