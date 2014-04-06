


class BaseOperation(object):

    enabled = False
    tag = None
    help_str = None

    @staticmethod
    def register_parser(subparsers):
        raise NotImplementedError("Abstract class (please overload this method)")

    @staticmethod
    def main(options):
        raise NotImplementedError("Abstract class (please overload this method)")

