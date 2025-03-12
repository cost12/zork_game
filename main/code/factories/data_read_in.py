import glob
import json
from typing import Any

from code.models.actors              import Direction
from code.models.action              import Action
from code.models.state               import Skill

from code.factories.factories import ItemFactory, NamedFactory, StateFactory, StateGraphFactory, StateDisconnectedGraphFactory, SkillSetFactory, CharacterFactory, LocationFactory, CharacterControlFactory

def __read_in_json(file:str) -> dict:
    with open(file) as contents:
        data = json.load(contents)
    return data

def __read_in_folder(folder:str) -> list[dict[str,Any]]:
    files = glob.glob(f"main/{folder}/*")
    return [__read_in_json(file) for file in files]

def read_in_directions(game:str) -> NamedFactory[Direction]:
    factory = NamedFactory[Direction]()
    folder = f"data/{game}/directions"
    data = __read_in_folder(folder)
    for d in data:
        factory.many_from_dict(d['data'])
    return factory

def read_in_actions(game:str) -> NamedFactory[Action]:
    factory = NamedFactory[Action]()
    folder = f"data/{game}/actions"
    data = __read_in_folder(folder)
    data = [data_dict for data_list in data for data_dict in data_list]
    factory.many_from_dict(data)
    return factory

def read_in_states(game:str, actions:NamedFactory[Action]) -> StateFactory:
    factory = StateFactory()
    folder = f"data/{game}/states"
    data = __read_in_folder(folder)
    data = [data_dict for data_list in data for data_dict in data_list]
    factory.many_from_dict(data, actions)
    return factory

def read_in_state_graphs(game:str, states:StateFactory, actions:NamedFactory[Action]) -> StateGraphFactory:
    factory = StateGraphFactory()
    folder = f"data/{game}/state_graphs"
    data = __read_in_folder(folder)
    data = [data_dict for data_list in data for data_dict in data_list]
    factory.many_from_dict(data, states, actions)
    return factory

def read_in_state_disconnected_graphs(game:str, state_graphs:StateGraphFactory) -> StateDisconnectedGraphFactory:
    factory = StateDisconnectedGraphFactory()
    folder = f"data/{game}/state_disconnected_graphs"
    data = __read_in_folder(folder)
    factory.many_from_dict(data[0], state_graphs)
    return factory

def read_in_items(game:str, state_graphs:StateDisconnectedGraphFactory, actions:NamedFactory[Action], states:StateFactory) -> ItemFactory:
    factory = ItemFactory()
    folder = f"data/{game}/items"
    data = __read_in_folder(folder)
    factory.many_from_dict(data, state_graphs, actions, states)
    return factory

def read_in_skills(game:str) -> NamedFactory[Skill]:
    factory = NamedFactory[Skill]()
    folder  = f"data/{game}/skills"
    data = __read_in_folder(folder)
    factory.many_from_dict(data[0])
    return factory

def read_in_skill_sets(game:str, skill_factory:NamedFactory[Skill]) -> SkillSetFactory:
    factory = SkillSetFactory()
    folder = f"data/{game}/skill_sets"
    data = __read_in_folder(folder)
    factory.many_from_dict(data[0], skill_factory)
    return factory

def read_in_characters(game:str, state_graphs:StateDisconnectedGraphFactory, skills_factory:NamedFactory[Skill], item_factory:ItemFactory, action_factory:NamedFactory[Action], state_factory:StateFactory) -> CharacterFactory:
    factory = CharacterFactory()
    folder = f"data/{game}/characters"
    data = __read_in_folder(folder)
    factory.many_from_dict(data, state_graphs, skills_factory, item_factory, action_factory, state_factory)
    return factory

def read_in_rooms(game:str, character_factory:CharacterFactory, item_factory:ItemFactory, direction_factory:NamedFactory[Direction], state_factory:StateFactory) -> LocationFactory:
    factory = LocationFactory()
    folder = f"data/{game}/rooms"
    data = __read_in_folder(folder)
    factory.many_from_dict(data, character_factory, item_factory, direction_factory, state_factory)
    return factory

def read_in_character_control(game:str, character_factory:CharacterFactory) -> CharacterControlFactory:
    factory = CharacterControlFactory()
    folder = f"data/{game}/character_control"
    data = __read_in_folder(folder)
    factory.many_from_dict(data[0], character_factory)
    return factory

def read_in_game_details(game:str) -> Any:
    file = f"main/data/{game}/game_details.json"
    return __read_in_json(file)

def read_in_game(game:str) -> tuple[LocationFactory, CharacterFactory, CharacterControlFactory, ItemFactory, NamedFactory[Action], NamedFactory[Direction], dict[str,Any]]:
    directions   = read_in_directions(game)
    actions      = read_in_actions(game)
    states       = read_in_states(game, actions)
    graphs       = read_in_state_graphs(game, states, actions)
    full_graphs  = read_in_state_disconnected_graphs(game, graphs)
    items        = read_in_items(game, full_graphs, actions, states)
    skills       = read_in_skills(game)
    skill_sets   = read_in_skill_sets(game, skills)
    characters   = read_in_characters(game, full_graphs, skill_sets, items, actions, states)
    rooms        = read_in_rooms(game, characters, items, directions, states)
    controllers  = read_in_character_control(game, characters)
    game_details = read_in_game_details(game)
    game_details['playable_characters'] = controllers.playable_characters()
    return rooms, characters, controllers, items, actions, directions, game_details
