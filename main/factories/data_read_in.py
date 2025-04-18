import glob
import json
from typing import Any

from models.named    import Action, Direction
from models.state    import Skill, Achievement
from utils.constants import *

from factories.factories import ItemFactory, NamedFactory, StateFactory, StateGraphFactory, SkillSetFactory, CharacterFactory, LocationFactory, CharacterControlFactory, LocationDetailFactory

def __read_in_json(file:str) -> dict:
    with open(file) as contents:
        data = json.load(contents)
    return data

def __read_in_folder(folder:str) -> list[dict[str,Any]]:
    files = glob.glob(f"main/{folder}/*.json")
    if len(files) == 0:
        print(f"Folder {folder} doesn't exist")
    output = []
    for file in files:
        try:
            output.append(__read_in_json(file))
        except json.JSONDecodeError as e:
            print(e)
            print(f"ERROR reading {file}")
        except UnicodeDecodeError as e:
            print(e)
            print(f"ERROR reading {file}")
    return output

def read_in_directions(game:str) -> NamedFactory[Direction]:
    factory = NamedFactory[Direction](Direction)
    folder = f"data/{game}/directions"
    data = __read_in_folder(folder)
    for d in data:
        factory.many_from_dict(d['data'])
    return factory

def read_in_actions(game:str) -> NamedFactory[Action]:
    factory = NamedFactory[Action](Action)
    folder = f"data/{game}/actions"
    data = __read_in_folder(folder)
    data = [data_dict for data_list in data for data_dict in data_list]
    factory.many_from_dict(data)
    return factory

def read_in_achievements(game:str) -> NamedFactory[Achievement]:
    factory = NamedFactory[Achievement](Achievement)
    folder = f"data/{game}/achievements"
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

def read_in_items(game:str, actions:NamedFactory[Action], states:StateFactory, state_graphs:StateGraphFactory) -> ItemFactory:
    factory = ItemFactory()
    folder = f"data/{game}/items"
    data = __read_in_folder(folder)
    factory.many_from_dict(data, actions, states, state_graphs)
    return factory

def read_in_skills(game:str) -> NamedFactory[Skill]:
    factory = NamedFactory[Skill](Skill)
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

def read_in_characters(game:str, skill_sets_factory:SkillSetFactory, action_factory:NamedFactory[Action], state_factory:StateFactory, achievement_factory:NamedFactory[Achievement], state_graph_factory:StateGraphFactory) -> CharacterFactory:
    factory = CharacterFactory()
    folder = f"data/{game}/characters"
    data = __read_in_folder(folder)
    factory.many_from_dict(data, skill_sets_factory, action_factory, state_factory, achievement_factory, state_graph_factory)
    return factory

def update_targets(game:str, items:ItemFactory, characters:CharacterFactory, details:LocationDetailFactory, locations:LocationFactory, states:StateFactory, actions:NamedFactory[Action], achievements:NamedFactory[Achievement]) -> None:
    folder = f"data/{game}/items"
    data = __read_in_folder(folder)
    items.update(data, characters, details, locations, states, actions, achievements)
    folder = f"data/{game}/characters"
    data = __read_in_folder(folder)
    characters.update(data, items, details, locations, states, actions, achievements)

def read_in_rooms(game:str, character_factory:CharacterFactory, item_factory:ItemFactory, direction_factory:NamedFactory[Direction], state_factory:StateFactory, achievement_factory:NamedFactory[Achievement]) -> tuple[LocationFactory,LocationDetailFactory]:
    factory = LocationFactory()
    folder = f"data/{game}/rooms"
    data = __read_in_folder(folder)
    _, detail_factory = factory.many_from_dict(data, character_factory, item_factory, direction_factory, state_factory, achievement_factory)
    return factory, detail_factory

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
    if DEBUG_READIN: print(f"Loaded {len(set(directions.aliases.values()))} directions")
    actions      = read_in_actions(game)
    if DEBUG_READIN: print(f"Loaded {len(set(actions.aliases.values()))} actions")
    achievements = read_in_achievements(game)
    if DEBUG_READIN: print(f"Loaded {len(set(achievements.aliases.values()))} achievements")
    states       = read_in_states(game, actions)
    if DEBUG_READIN: print(f"Loaded {len(set(states.states.values()))} states")
    graphs       = read_in_state_graphs(game, states, actions)
    if DEBUG_READIN: print(f"Loaded {len(set(graphs.aliases.values()))} graphs")
    items        = read_in_items(game, actions, states, graphs)
    if DEBUG_READIN: print(f"Loaded {len(set(items.aliases.values()))} items")
    skills       = read_in_skills(game)
    if DEBUG_READIN: print(f"Loaded {len(set(skills.aliases.values()))} skills")
    skill_sets   = read_in_skill_sets(game, skills)
    if DEBUG_READIN: print(f"Loaded {len(set(skill_sets.aliases.values()))} skill sets")
    characters   = read_in_characters(game, skill_sets, actions, states, achievements, graphs)
    if DEBUG_READIN: print(f"Loaded {len(set(characters.aliases.values()))} characters")
    rooms,details = read_in_rooms(game, characters, items, directions, states, achievements)
    if DEBUG_READIN: print(f"Loaded {len(set(rooms.aliases.values()))} rooms")
    if DEBUG_READIN: print(f"Loaded {len(set(details.aliases.values()))} details")
    update_targets(game, items, characters, details, rooms, states, actions, achievements)
    controllers  = read_in_character_control(game, characters)
    game_details = read_in_game_details(game)
    game_details['playable_characters'] = controllers.playable_characters()
    return rooms, characters, controllers, items, actions, directions, game_details
