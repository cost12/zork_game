from importlib import import_module
from typing    import Any
import pkgutil
import json

import data.game1
from data.game1.character_control.character_control import get_character_control
from factories.factories                            import CharacterControlFactory
from utils.relator                                  import NameFinder
from readin.stand_in                                import replace_standins

def __read_in_json(file:str) -> dict:
    with open(file) as contents:
        info = json.load(contents)
        return info

def read_in_game_details(game:str) -> dict:
    file = f"main/data/{game}/game_details.json"
    return __read_in_json(file)

def get_level1() -> tuple[NameFinder, CharacterControlFactory, dict[str,Any]]:
    name_space = NameFinder()

    modules = ['directions', 'actions', 'achievements', 'states', 'state_graphs', 'items', 'skills', 'skill_sets', 'characters', 'rooms']
    for module in modules:
        try:
            imported_module = import_module(f'data.game1.{module}')
            sub_modules = [name for _, name, _ in pkgutil.iter_modules(imported_module.__path__)]
            print(sub_modules)
            for sub_module in sub_modules:
                try:
                    imported_sub_module = import_module(f"data.game1.{module}.{sub_module}")
                    imported_sub_module.add_to_name_space(name_space)
                except ImportError as e:
                    print(f'Error importing {module}.{sub_module} in level 1')
                    raise e
        except ImportError as e:
            print(f'Error importing {module} in level 1')
            raise e

    replace_standins(name_space)
    controllers = get_character_control(name_space)
    game_details = read_in_game_details('game1')
    game_details['playable_characters'] = controllers.playable_characters()
    return name_space, controllers, game_details
