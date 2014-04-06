


class BaseOperation(object):

    enabled = False
    tag = None
    help_str = None

    @staticmethod
    def register_parser(parser):
        raise NotImplementedError("Abstract class (please overload this method)")

    @staticmethod
    def main(options):
        raise NotImplementedError("Abstract class (please overload this method)")


class ListOperations(BaseOperation):
    enabled = True
    tag = 'list'
    help_str = 'list all operations'

    @staticmethod
    def register_parser(parser):
        pass

    @staticmethod
    def main(options):
        from stocker.SEP.operations import all_operations

        print("tag\tenabled\tclass\t\tdescription")
        print('===========================================')
        for operation in all_operations:
            print("%s\t%s\t%s\t\t%s" % (operation.tag, operation.enabled, operation.__name__, operation.help_str))



