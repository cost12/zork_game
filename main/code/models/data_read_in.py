from code.models.room import Room
from code.models.item import Item, Inventory
from code.models.character import Character
from code.models.action import Action
from code.controls.character_control import GameCharacter, CommandLineController, NPCController

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

def read_in_room(data:dict[str,Any], actions:dict[str,Action], characters:dict[str,Character], items:dict[str,Item]) -> tuple[Room, bool]:
    start = False
    if 'start' in data:
        start = True
    name = data['name']
    description = data['description']
    room_characters = []
    if 'characters' in data:
        for character_name in data['characters']:
            room_characters.append(characters[character_name])
    room_items = []
    if 'items' in data:
        for item_name in data['items']:
            room_items.append(items[item_name])
    room_actions = []
    if 'actions' in data:
        for action_name in data['actions']:
            room_actions.append(actions[action_name])
    return Room(name, description, None, room_items, room_characters, room_actions), start

def read_in_rooms(game:str, actions:dict[str,Action], characters:dict[str,Character], items:dict[str,Item]) -> tuple[list[Room],list[Room]]:
    folder = f"data/{game}/rooms"
    data = __read_in_folder(folder)
    rooms = [read_in_room(room_data, actions, characters, items) for room_data in data]
    start_rooms = [room for room,start in rooms if start]
    rooms = [room for room,_ in rooms]
    return rooms, start_rooms

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

def read_in_game_details(game:str) -> Any:
    file = f"main/data/{game}/game_details.json"
    return __read_in_json(file)

def read_in_game(game:str) -> tuple[list[Room],list[Room],list[GameCharacter],list[Item],list[Action],dict[str,Any]]:
    actions = read_in_actions(game)
    action_dict = {action.get_name():action for action in actions} 
    items = read_in_items(game, action_dict)
    item_dict = {item.get_name():item for item in items}
    characters = read_in_characters(game, action_dict)
    character_dict = {character.get_name():character for character in characters}
    rooms, start_rooms = read_in_rooms(game, action_dict, character_dict, item_dict)
    room_dict = {room.get_name():room for room in rooms}
    game_characters, playable_characters = read_in_characters_details(game, room_dict, character_dict, item_dict)
    game_details = read_in_game_details(game)
    game_details['playable_characters'] = playable_characters
    return rooms, start_rooms, game_characters, items, actions, game_details
