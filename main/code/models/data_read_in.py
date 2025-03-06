from code.models.room import Room, Direction, Exit
from code.models.item import Item, Inventory
from code.models.character import Character
from code.models.action import Action
from code.controls.character_control import GameCharacter, GameRoom, CommandLineController, NPCController

import glob
import json
from typing import Any

def __read_in_json(file:str) -> dict:
    with open(file) as contents:
        data = json.load(contents)
    return data

def __read_in_folder(folder:str) -> list[dict[str,Any]]:
    files = glob.glob(f"main/{folder}/*")
    return [__read_in_json(file) for file in files]

def read_in_direction_dict(data:dict[str,list[dict[str,Any]]]) -> list[Direction]:
    directions = list[Direction]()
    for direction_data in data['data']:
        name = direction_data['name']
        aliases = direction_data['aliases']
        directions.append(Direction.make_direction(name, aliases))
    return directions

def read_in_directions(game:str) -> list[Direction]:
    folder = f"data/{game}/directions"
    data = __read_in_folder(folder)
    directions = list[Direction]()
    for direction_dict in data:
        directions.extend(read_in_direction_dict(direction_dict))
    return directions

def read_in_action(data:dict[str,Any]) -> Action:
    name = data['name']
    aliases = data['aliases']
    return Action(name, aliases)

def read_in_actions(game:str) -> list[Action]:
    folder = f"data/{game}/actions"
    data = __read_in_folder(folder)
    return [read_in_action(action_data) for action_data in data]

def read_in_item(data:dict[str,Any], actions:dict[str,Action]) -> Item:
    name = data['name']
    description = data['description']
    weight = data['weight']
    value = data['value']
    item_actions = []
    if 'actions' in data:
        for action_name in data['actions']:
            item_actions.append(actions[action_name])
    return Item(name, description, weight, value, item_actions)

def read_in_items(game:str, actions:dict[str,Action]) -> list[Item]:
    folder = f"data/{game}/items"
    data = __read_in_folder(folder)
    return [read_in_item(item_data, actions) for item_data in data]

def read_in_character(data:dict[str,Any], actions:dict[str,Action]) -> Character:
    name = data['name']
    type = data['type']
    description = data['description']
    character_actions = []
    if 'actions' in data:
        for action_name in data['actions']:
            character_actions.append(actions[action_name])
    return Character(name, type, description, character_actions)

def read_in_characters(game:str, actions:dict[str,Action]) -> list[Character]:
    folder = f"data/{game}/characters"
    data = __read_in_folder(folder)
    return [read_in_character(character_data, actions) for character_data in data]

def read_in_room(data:dict[str,Any], actions:dict[str,Action]) -> Room:
    name = data['name']
    description = data['description']
    room_actions = []
    if 'actions' in data:
        for action_name in data['actions']:
            room_actions.append(actions[action_name])
    return Room(name, description, room_actions)

def read_in_rooms(game:str, actions:dict[str,Action]) -> list[Room]:
    folder = f"data/{game}/rooms"
    data = __read_in_folder(folder)
    return [read_in_room(room_data, actions) for room_data in data]

def read_in_inventory(data:dict[str,Any], items:dict[str,Item]) -> Inventory:
    item_limit = data['item_limit']
    weight_limit = data['weight_limit']
    inventory_items = []
    if 'item' in data:
        for item_name in data['items']:
            inventory_items.append(items[item_name])
    return Inventory(item_limit,  weight_limit, inventory_items)

def read_in_character_details(data:dict[str,Any], rooms:dict[str,Room], characters:dict[str,Character], items:dict[str,Item]) -> tuple[GameCharacter, bool]:
    character = characters[data['character']]
    controller = CommandLineController() if data['control_type'] == 'user' else NPCController()
    spawn_room = rooms[data['spawn_room']]
    inventory = read_in_inventory(data['inventory'], items)
    return GameCharacter(character, spawn_room, controller, inventory), data['control_type'] == 'user'

def read_in_characters_details(game:str, rooms:dict[str,Room], characters:dict[str,Character], items:dict[str,Item]) -> tuple[list[GameCharacter],int]:
    folder = f"data/{game}/character_details"
    data = __read_in_folder(folder)
    details = [read_in_character_details(character_data, rooms, characters, items) for character_data in data]
    game_characters = [game_character for game_character,_ in details]
    playable_characters = sum([1 for _,user in details if user])
    return game_characters, playable_characters

def read_in_exits(data:list[dict[str,Any]], directions:dict[str,Direction], rooms:dict[str,Room]) -> dict[Direction,Exit]:
    exits = dict[Direction,Exit]()
    for exit_data in data:
        name = exit_data['name']
        description = exit_data['description']
        direction = directions[exit_data['direction']]
        end = rooms[exit_data['end']]
        exits[direction] = Exit(name, description, end)
    return exits

def read_in_room_details(data:dict[str,Any], directions:dict[str,Direction], rooms:dict[str,Room], characters:dict[str,GameCharacter], items:dict[str,Item]) -> GameRoom:
    start = False
    if 'start' in data:
        start = True
    room = rooms[data['room']]
    exits = read_in_exits(data['exits'], directions, rooms)
    room_characters = []
    room_items = []
    if 'items' in data:
        for item_name in data['items']:
            room_items.append(items[item_name])
    game_room = GameRoom(room, exits, room_characters, room_items, start)
    if 'characters' in data:
        for character_name in data['characters']:
            character = characters[character_name]
            game_room.add_character(character)
            character.set_current_room(game_room)
    return game_room

def read_in_rooms_details(game:str, directions:dict[str,Direction], rooms:dict[str,Room],  characters:dict[str,GameCharacter], items:dict[str,Item]) -> list[GameRoom]:
    folder = f"data/{game}/room_details"
    data = __read_in_folder(folder)
    return [read_in_room_details(room_data, directions, rooms, characters, items) for room_data in data]

def read_in_game_details(game:str) -> Any:
    file = f"main/data/{game}/game_details.json"
    return __read_in_json(file)

def read_in_game(game:str) -> tuple[list[GameRoom],list[GameCharacter],list[Action],list[Item],list[Direction],dict[str,Any]]:
    directions = read_in_directions(game)
    direction_dict = {direction.get_name():direction for direction in directions}
    actions = read_in_actions(game)
    action_dict = {action.get_name():action for action in actions} 
    items = read_in_items(game, action_dict)
    item_dict = {item.get_name():item for item in items}
    characters = read_in_characters(game, action_dict)
    character_dict = {character.get_name():character for character in characters}
    rooms = read_in_rooms(game, action_dict)
    room_dict = {room.get_name():room for room in rooms}
    game_characters, playable_characters = read_in_characters_details(game, room_dict, character_dict, item_dict)
    game_character_dict = {game_character.get_name():game_character for game_character in game_characters}
    game_rooms = read_in_rooms_details(game, direction_dict, room_dict, game_character_dict, item_dict)
    game_details = read_in_game_details(game)
    game_details['playable_characters'] = playable_characters
    return game_rooms, game_characters, actions, items, directions, game_details
