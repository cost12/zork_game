from importlib import import_module
import pkgutil

import data.aagame1
from utils.relator   import NameFinder
from readin.stand_in import replace_standins

def get_level1() -> NameFinder:
    name_space = NameFinder()

    modules = ['directions', 'actions', 'achievements', 'states', 'state_graphs', 'items', 'skills', 'skill_sets', 'characters']#, 'rooms', 'character_control']
    for module in modules:
        try:
            imported_module = import_module(f'data.aagame1.{module}')
            sub_modules = [name for _, name, _ in pkgutil.iter_modules(imported_module.__path__)]
            print(sub_modules)
            for sub_module in sub_modules:
                try:
                    imported_sub_module = import_module(f"data.aagame1.{module}.{sub_module}")
                    imported_sub_module.add_to_name_space(name_space)
                except ImportError as e:
                    print(f'Error importing {module}.{sub_module} in level 1')
                    raise e
        except ImportError as e:
            print(f'Error importing {module} in level 1')
            raise e

    replace_standins(name_space)
    return name_space, None, None, None, None
