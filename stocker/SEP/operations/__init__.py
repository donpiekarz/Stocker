import inspect
import pkgutil
import sys

from stocker.SEP.operations.BaseOperation import BaseOperation


def find_operations(path):
    available_operations = {}
    all_operations = set()

    for module in pkgutil.iter_modules(path):
        module_name = ''.join([__name__, '.', module[1]])
        __import__(module_name)

        is_subclass_of_base_operation = lambda c: inspect.isclass(c) and issubclass(c,
                                                                                    BaseOperation) and c is not BaseOperation
        for _, cls in inspect.getmembers(sys.modules[module_name], is_subclass_of_base_operation):
            all_operations.add(cls)
            is_enabled = getattr(cls, 'enabled', False)
            if is_enabled:
                tag = getattr(cls, 'tag', None)
                help_str = getattr(cls, 'help_str', None)
                assert tag is not None, "missing tag (please override)"
                assert help_str is not None, "missing help_str (please override)"

                available_operations[tag] = cls

    return available_operations, all_operations


available_operations, all_operations = find_operations(__path__)
