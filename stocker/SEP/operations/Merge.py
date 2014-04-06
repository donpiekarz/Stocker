from stocker.SEP.operations.BaseOperation import BaseOperation


class Merge(BaseOperation):
    enabled = True
    tag = 'merge'
    help_str = 'merge two (or more) streams'

    @staticmethod
    def register_parser(parser):
        parser.add_argument('a', type=int, help='a help')

    @staticmethod
    def main(options):
        print("inside merge")
