from typing import Any, Optional
from dataclasses import dataclass

from code.models.character import Character
from code.models.room import Room, Direction, Exit
from code.models.item import Item, Inventory
from code.models.action import Action
from code.utils.graph import Node, NodeGraph
import code.views.string_views as views
from code.controls.translate import Translator, get_input_translator

@dataclass(frozen=True)
class Feedback:
    feedback:str

    def as_string(self) -> str:
        return self.feedback

class CharacterController:

    def __init__(self):
        pass

    def make_move(self, moves:int, turns:int, score:int) -> str:
        pass

    def feedback(self, feedback:Feedback) -> None:
        pass

class NPCController(CharacterController):
    def __init__(self):
        pass

    def make_move(self, moves:int, turns:int, score:int) -> str:
        return 'wait'

    def feedback(self, feedback:Feedback) -> None:
        pass

class CommandLineController(CharacterController):

    def __init__(self):
        pass

    def make_move(self, moves:int, turns:int, score:int) -> str:
        return input(views.input_prompt(moves,turns,score))
    
    def feedback(self, feedback:Feedback) -> None:
        print(feedback.as_string())

class GameCharacter:

    def __init__(self, character:Character, spawn_room:Room, controller:CharacterController, inventory:Inventory):
        self.character = character
        self.spawn_room = spawn_room
        self.controller = controller
        self.inventory = inventory
        self.current_room = None
        self.moves = 0
        self.turns = 0
        self.score = 0

    #########################################################################################
    # Controller Functions
    #########################################################################################
    def make_move(self) -> str:
        return self.controller.make_move(self.get_moves(), self.get_turns(), self.get_score())
    
    def feedback(self, feedback) -> None:
        self.controller.feedback(feedback) 
    
    ########################################################################################
    # Getters
    ########################################################################################
    def get_name(self) -> str:
        return self.character.get_name()
    
    def get_description(self) -> str:
        return self.character.get_description()
    
    def get_moves(self) -> int:
        return self.moves
    
    def get_turns(self) -> int:
        return self.turns
    
    def get_score(self) -> int:
        return self.score
    
    def get_current_room(self) -> 'GameRoom':
        return self.current_room
    
    def can_see(self, item:Item) -> bool:
        return self.inventory.contains(item) or self.current_room.contains(item)
    
    ########################################################################################
    # Setters
    ########################################################################################
    def set_current_room(self, room:'GameRoom') -> None:
        self.current_room = room
    
class GameRoom(Node[Direction]):

    def __init__(self, room:Room, exits:dict[Direction, Exit], characters:list[GameCharacter], items:list[Item], is_user_start_room:bool=False):
        self.room = room
        self.exits = exits
        self.characters = {character.get_name():character for character in characters}
        self.items = {item.get_name():item for item in items}
        self.is_user_start_room = is_user_start_room

    ########################################################################################
    # Node Functions
    ########################################################################################
    def get_child(self, edge:Direction) -> Optional['GameRoom']:
        if edge in self.exits:
            exit = self.exits[edge]
            if exit.can_exit():
                return self.exits[edge].get_end()
        return None
    
    def get_edges(self) -> list[Direction]:
        return [direction for direction,exit in self.exits.items() if exit.can_exit()]

    ########################################################################################
    # Getters
    ########################################################################################
    def get_name(self) -> str:
        return self.room.get_name()
    
    def get_description(self, character:GameCharacter) -> str:
        description = self.room.get_description()
        if len(self.items) > 0:
            description += "\nIn this room you find "
            description += ", ".join([item.get_description() for item in self.items.values()]) + "."
        if len(self.characters) > 1:
            description += "\nYou see "
            description += ", ".join([char.get_description() for name,char in self.characters.items() if not name.lower() == character.get_name().lower()]) + "."
        if len(self.exits) > 0:
            for direction,exit in self.exits.items():
                description += f"\nTo the {direction.get_name()} {exit.get_description()}."
        return description
    
    def get_characters(self) -> list[GameCharacter]:
        return list(self.characters.values())
    
    def get_items(self) -> list[Item]:
        return list(self.items.values())
    
    def get_exit(self, direction:Direction) -> Optional[Exit]:
        return self.exits[direction]

    def is_start_room(self) -> bool:
        return self.is_user_start_room
    
    def contains(self, item:Item) -> bool:
        return item in list(self.items.values())
    
    ########################################################################################
    # Mutators
    ########################################################################################
    def remove_character(self, character:GameCharacter) -> None:
        del self.characters[character.get_name()]

    def add_character(self, character:GameCharacter) -> None:
        self.characters[character.get_name()] = character

class GameState:

    def __init__(self, rooms:list[GameRoom], characters:list[GameCharacter], extra_characters:list[Character], actions:list[Action], items:list[Item], directions:list[Direction]):
        self.character_order = characters
        self.translator = get_input_translator()
        
        i = 0
        start_rooms = [room for room in rooms if room.is_start_room()]
        for character in extra_characters:
            start_room = start_rooms[i%len(start_rooms)]
            new_character = GameCharacter(character, start_room, CommandLineController(), Inventory(10,10))
            new_character.set_current_room(start_room)
            self.character_order.append(new_character)
            i += 1
        self.current_turn = 0
        self.moves = 0

        self.all_actions = dict[str,Action]()
        for action in actions:
            for alias in action.get_aliases():
                if alias.lower() in self.all_actions:
                    print(f"Warning: {alias.lower()} is ambiguous, multiple actions have this name.")
                self.all_actions[alias.lower()] = action

        self.all_rooms = dict[str,GameRoom]()
        for room in rooms:
            for alias in room.room.get_aliases():
                if alias.lower() in self.all_rooms:
                    print(f"Warning: {alias.lower()} is ambiguous, multiple rooms have this name.")
                self.all_rooms[alias.lower()] = room

        self.all_characters = dict[str,GameCharacter]()
        for character in self.character_order:
            for alias in character.character.get_aliases():
                if alias.lower() in self.all_characters:
                    print(f"Warning: {alias.lower()} is ambiguous, multiple characters have this name.")
                self.all_characters[alias.lower()] = character

        self.all_directions = dict[str,Direction]()
        for direction in directions:
            for alias in direction.get_aliases():
                if alias.lower() in self.all_directions:
                    print(f"Warning: {alias.lower()} is ambiguous, multiple directions have this name.")
                self.all_directions[alias.lower()] = direction

        self.all_items = dict[str,Item]()
        for item in items:
            for alias in item.get_aliases():
                if alias.lower() in self.all_items:
                    print(f"Warning: {alias.lower()} is ambiguous, multiple items have this name.")
                self.all_items[alias.lower()] = item

    def get_available_actions(self, character:Character) -> list[tuple[str,set]]:
        pass

    def get_available_targets(self, character:Character) -> list[tuple[str,set]]:
        pass

    def get_room(self, character:Character) -> Room:
        pass

    def get_start_room(self, character:Character) -> Room:
        pass

    def get_score(self, character:Character) -> int:
        pass

    def get_moves(self, character:Character) -> int:
        pass

    def whose_turn(self) -> GameCharacter:
        return self.character_order[self.current_turn%len(self.character_order)]

    def game_over(self) -> bool:
        pass

    def translate(self, user_input:str) -> tuple[Action,list]:
        return self.translator.interpret(user_input, self.all_actions, self.all_characters, self.all_rooms, self.all_items, self.all_directions)
    
    ###########################################################################
    # Main driver
    ###########################################################################
    def play(self) -> None:
        while not self.game_over():
            character = self.whose_turn()
            print(f"Turn: {character.get_name()}")
            user_input = character.make_move()
            print(f"Input: {user_input}")
            action, inputs = self.translate(user_input)
            print(f"Translation: {action} {inputs}")
            feedback = self.action(character, action, inputs)
            print(f"Feedback: {feedback}")
            character.feedback(feedback)

    ###########################################################################
    # Actions
    ###########################################################################
    def action(self, character:GameCharacter, action:Action, inputs:tuple) -> Feedback:
        feedback = None
        if action == 'error':
            return Feedback(inputs)
        if 'walk' in action.get_aliases():
            feedback = self.walk(character, inputs[0])
        elif 'look' in action.get_aliases():
            if len(inputs) > 0:
                feedback = self.look(character, inputs[0])
            else:
                feedback = self.look(character)
        elif 'wait' in action.get_aliases():
            feedback = Feedback("Time passes.")
        self.current_turn += 1
        self.moves += 1
        return feedback

    def walk(self, character:GameCharacter, direction:Direction) -> Feedback:
        room = character.get_current_room()
        exit = room.get_exit(direction)
        if exit is None:
            return Feedback(f"There is nothing {direction.get_name()}.")
        elif isinstance(exit, Exit) and exit.can_exit():
            room.remove_character(character)
            new_room_name = exit.get_end().get_name().lower()
            new_room = self.all_rooms[new_room_name]
            character.set_current_room(new_room)
            new_room.add_character(character)
            return self.look(character)
        else:
            return Feedback(exit.get_description())
        
    def look(self, character:GameCharacter, target:Optional[Item]=None) -> Feedback:
        if target is None:
            return Feedback(character.get_current_room().get_description(character))
        else:
            if character.can_see(target):
                return Feedback(target.get_description())
            else:
                return Feedback(f"There is no {target.get_name()} here.")
