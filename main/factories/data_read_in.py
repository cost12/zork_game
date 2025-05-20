import glob
import json
from typing import Any

from utils.relator   import NameFinder
from models.named    import Action, Direction
from models.state    import Skill, State, StateGraph, SkillSet, StateGroup, Achievement
from models.actors   import Target, Actor, Location
from utils.constants import *

from factories.factories import CharacterControlFactory
import factories.factories as factories

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
            to_add = __read_in_json(file)
            if isinstance(to_add, list):
                output.extend(to_add)
            else:
                output.append(to_add)
        except json.JSONDecodeError as e:
            print(e)
            print(f"ERROR reading {file}")
        except UnicodeDecodeError as e:
            print(e)
            print(f"ERROR reading {file}")
    return output

def read_in_directions(game:str, name_space:NameFinder) -> None:
    folder     = f"data/{game}/directions"
    data       = __read_in_folder(folder)
    inputs     = factories.many_from_dict_named(data)
    directions = [Direction(**kwargs) for kwargs in inputs]
    success    = name_space.add_many(directions)
    if DEBUG_READIN: print(f"Loaded {len(success)} directions")
    fails = [kwargs['name'] for s,kwargs in zip(success,inputs) if not s]
    if len(fails) > 0: print(f"Failed to add: {fails}")
    assert all(success)
    
def read_in_actions(game:str, name_space:NameFinder) -> None:
    folder  = f"data/{game}/actions"
    data    = __read_in_folder(folder)
    inputs  = factories.many_from_dict_action(data)
    actions = [Action(**kwargs) for kwargs in inputs]
    success = name_space.add_many(actions)
    if DEBUG_READIN: print(f"Loaded {len(success)} actions")
    fails = [kwargs['name'] for s,kwargs in zip(success,inputs) if not s]
    if len(fails) > 0: print(f"Failed to add: {fails}")
    assert all(success)

def read_in_achievements(game:str, name_space:NameFinder) -> None:
    folder  = f"data/{game}/achievements"
    data    = __read_in_folder(folder)
    inputs  = factories.many_from_dict_named(data)
    achievements = [Achievement(**kwargs) for kwargs in inputs]
    success = name_space.add_many(achievements)
    if DEBUG_READIN: print(f"Loaded {len(success)} achievements")
    fails = [kwargs['name'] for s,kwargs in zip(success,inputs) if not s]
    if len(fails) > 0: print(f"Failed to add: {fails}")
    assert all(success)

def read_in_states(game:str, name_space:NameFinder) -> None:
    folder  = f"data/{game}/states"
    data    = __read_in_folder(folder)
    inputs  = factories.many_from_dict_state(data, name_space)
    states  = [State.create_state(**kwargs) for kwargs in inputs]
    success = name_space.add_many(states)
    if DEBUG_READIN: print(f"Loaded {len(success)} states")
    fails = [kwargs['name'] for s,kwargs in zip(success,inputs) if not s]
    if len(fails) > 0: print(f"Failed to add: {fails}")
    assert all(success)

def read_in_state_graphs(game:str, name_space:NameFinder, setup_space:NameFinder) -> None:
    folder  = f"data/{game}/state_graphs"
    data    = __read_in_folder(folder)
    groups_data  = [sgdict for gdict in data if 'state_groups' in gdict for sgdict in gdict['state_groups']]
    group_inputs = factories.many_from_dict_state_group(groups_data, name_space)
    groups  = [StateGroup(**kwargs) for kwargs in group_inputs]
    success = setup_space.add_many(groups)
    if DEBUG_READIN: print(f"Loaded {len(success)} state groups")
    fails   = [kwargs['name'] for s,kwargs in zip(success,group_inputs) if not s]
    data    = [gdict for gdict in data if 'state_groups' not in gdict]
    inputs  = factories.many_from_dict_state_graph(data, name_space, setup_space)
    sgs     = [StateGraph(**kwargs) for kwargs in inputs]
    success = setup_space.add_many(sgs)
    if DEBUG_READIN: print(f"Loaded {len(success)} state graphs")
    fails = [kwargs['name'] for s,kwargs in zip(success,inputs) if not s]
    if len(fails) > 0: print(f"Failed to add: {fails}")
    assert all(success)

def read_in_items(game:str, name_space:NameFinder, setup_space:NameFinder) -> None:
    folder  = f"data/{game}/items"
    data    = __read_in_folder(folder)
    inputs  = factories.many_from_dict_item(data, name_space, setup_space)
    items   = [Target(**kwargs) for kwargs in inputs]
    success = name_space.add_many(items)
    if DEBUG_READIN: print(f"Loaded {len(success)} items")
    fails = [kwargs['name'] for s,kwargs in zip(success,inputs) if not s]
    if len(fails) > 0: print(f"Failed to add: {fails}")
    assert all(success)

def read_in_skills(game:str, name_space:NameFinder) -> None:
    folder  = f"data/{game}/skills"
    data    = __read_in_folder(folder)
    inputs  = factories.many_from_dict_named(data)
    skills  = [Skill(**kwargs) for kwargs in inputs]
    success = name_space.add_many(skills)
    if DEBUG_READIN: print(f"Loaded {len(success)} skills")
    fails = [kwargs['name'] for s,kwargs in zip(success,inputs) if not s]
    if len(fails) > 0: print(f"Failed to add: {fails}")
    assert all(success)

def read_in_skill_sets(game:str, name_space:NameFinder) -> None:
    folder  = f"data/{game}/skill_sets"
    data    = __read_in_folder(folder)
    inputs  = factories.many_from_dict_named(data)
    skill_sets = [SkillSet(**kwargs) for kwargs in inputs]
    success = name_space.add_many(skill_sets)
    if DEBUG_READIN: print(f"Loaded {len(success)} skill sets")
    fails = [kwargs['name'] for s,kwargs in zip(success,inputs) if not s]
    if len(fails) > 0: print(f"Failed to add: {fails}")
    assert all(success)

def read_in_characters(game:str, name_space:NameFinder, setup_space:NameFinder) -> None:
    folder  = f"data/{game}/characters"
    data    = __read_in_folder(folder)
    inputs  = factories.many_from_dict_character(data, name_space, setup_space)
    characters = [Actor(**kwargs) for kwargs in inputs]
    success = name_space.add_many(characters)
    if DEBUG_READIN: print(f"Loaded {len(success)} characters")
    fails = [kwargs['id'] for s,kwargs in zip(success,inputs) if not s]
    if len(fails) > 0: print(f"Failed to add: {fails}")
    assert all(success)

def read_in_rooms(game:str, name_space:NameFinder, setup_space:NameFinder) -> None:
    folder  = f"data/{game}/rooms"
    data    = __read_in_folder(folder)
    inputs  = factories.many_from_dict_location(data, name_space, setup_space)
    rooms   = [Location(**kwargs) for kwargs in inputs]
    success = name_space.add_many(rooms)
    if DEBUG_READIN: print(f"Loaded {len(success)} rooms")
    fails = [kwargs['name'] for s,kwargs in zip(success,inputs) if not s]
    if len(fails) > 0: print(f"Failed to add: {fails}")
    assert all(success)

def updates(game:str, name_space:NameFinder, setup_space:NameFinder) -> None:
    folder = f"data/{game}/items"
    data   = __read_in_folder(folder)
    factories.update_items(data, name_space, setup_space)
    if DEBUG_READIN: print("Items updated")
    folder = f"data/{game}/characters"
    data   = __read_in_folder(folder)
    factories.update_characters(data, name_space, setup_space)
    if DEBUG_READIN: print("Characters updated")
    folder = f"data/{game}/rooms"
    data   = __read_in_folder(folder)
    factories.update_locations(data, name_space, setup_space)
    if DEBUG_READIN: print("Locations updated")

def read_in_character_control(game:str, name_space:NameFinder) -> CharacterControlFactory:
    factory = CharacterControlFactory()
    folder  = f"data/{game}/character_control"
    data    = __read_in_folder(folder)
    factory.many_from_dict(data, name_space)
    return factory

def read_in_game_details(game:str) -> Any:
    file = f"main/data/{game}/game_details.json"
    return __read_in_json(file)

def read_in_game(game:str) -> tuple[NameFinder, NameFinder, CharacterControlFactory, dict[str,Any]]:
    name_space  = NameFinder()
    setup_space = NameFinder()
    read_in_directions  (game, name_space)
    read_in_actions     (game, name_space)
    read_in_achievements(game, name_space)
    read_in_states      (game, name_space)
    read_in_state_graphs(game, name_space, setup_space)
    read_in_items       (game, name_space, setup_space)
    read_in_skills      (game, name_space)
    read_in_skill_sets  (game, name_space)
    read_in_characters  (game, name_space, setup_space)
    read_in_rooms       (game, name_space, setup_space)
    updates             (game, name_space, setup_space)

    controllers  = read_in_character_control(game, name_space)
    game_details = read_in_game_details(game)
    game_details['playable_characters'] = controllers.playable_characters()
    return name_space, setup_space, controllers, game_details
