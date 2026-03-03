from importlib import import_module
from typing    import Any
import pkgutil
import json
import logging

import data.game1 # pylint: disable=unused-import
from data.game1.character_control.character_control import get_character_control
from data.game1.item_tree                           import get_item_tree
from models.actors                                  import World, WorldMap
from factories.factories                            import CharacterControlFactory
from utils.relator                                  import NameFinder
from readin.stand_in                                import replace_standins

logger = logging.getLogger(__name__)

def __read_in_json(file:str) -> dict:
    with open(file, encoding='utf-8') as contents:
        info = json.load(contents)
        return info

def read_in_game_details(game:str) -> dict:
    file = f"main/data/{game}/game_details.json"
    return __read_in_json(file)

def get_level1() -> tuple[World, NameFinder, CharacterControlFactory, dict[str,Any]]:
    name_space = NameFinder()

    modules = ['directions', 'actions', 'achievements', 'states', 'state_graphs', 'items', 'skills', 'skill_sets', 'characters', 'rooms', 'paths']
    for module in modules:
        logger.debug(module)
        try:
            imported_module = import_module(f'data.game1.{module}')
            sub_modules = [name for _, name, _ in pkgutil.iter_modules(imported_module.__path__)]
            logger.debug(sub_modules)
            for sub_module in sub_modules:
                try:
                    imported_sub_module = import_module(f"data.game1.{module}.{sub_module}")
                    imported_sub_module.add_to_name_space(name_space)
                except ImportError as e:
                    logger.debug('Error importing %s.%s in level 1', module, sub_module)
                    raise e
        except ImportError as e:
            logger.debug('Error importing %s in level 1', module)
            raise e

    replace_standins(name_space)
    world_map = WorldMap()
    for path in name_space.get_from_name(category='path'):
        world_map = world_map.add_path(path)
    world = World(init_locations=get_item_tree(name_space), init_map=world_map)
    controllers = get_character_control(name_space)
    game_details = read_in_game_details('game1')
    game_details['playable_characters'] = controllers.playable_characters()
    return world, name_space, controllers, game_details
