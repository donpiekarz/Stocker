
import inspect
import pkgutil
import sys

from stocker.SEP.operations.BaseOperation import BaseOperation

def find_operations(path):
    available_operations = set()
    all_operations = set()

    for module in pkgutil.iter_modules(path):
        module_name = ''.join([__name__, '.', module[1]])
        __import__(module_name)

        is_subclass_of_base_operation = lambda c: inspect.isclass(c) and issubclass(c, BaseOperation)
        for _, cls in inspect.getmembers(sys.modules[module_name], is_subclass_of_base_operation):
            all_operations.add(cls)
            is_enabled = getattr(cls, 'enabled', False)
            if is_enabled:
                available_operations.add(cls)

    return available_operations, all_operations

available_operations, all_operations = find_operations(__path__)

