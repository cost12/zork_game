from code.models.character import Character
from code.models.room import Room
from code.models.item import Item, Inventory
from code.models.action import Action
import code.views.string_views as views

class CharacterController:

    def __init__(self):
        pass

    def make_move(self) -> str:
        pass

    def feedback(self, feedback) -> None:
        pass

class NPCController(CharacterController):
    def __init__(self):
        pass

    def make_move(self) -> str:
        return 'end turn'

    def feedback(self, feedback) -> None:
        pass

class CommandLineController(CharacterController):

    def __init__(self):
        pass

    def make_move(self) -> str:
        return input(views.input_prompt())
    
    def feedback(self, feedback) -> None:
        print(feedback)

class GameCharacter:

    def __init__(self, character:Character, spawn_room:Room, controller:CharacterController, inventory:Inventory):
        self.character = character
        self.spawn_room = spawn_room
        self.controller = controller
        self.inventory = inventory
        self.moves = 0
        self.turns = 0
        self.score = 0

    def get_controller(self) -> CharacterController:
        return self.controller

class GameState:

    def __init__(self, rooms:list[Room], start_rooms:list[Room], characters:list[GameCharacter], extra_characters:list[Character], actions:list[Action]):
        assert len(rooms) > 0 and len(characters) > 0
        self.rooms = {room.get_name():room for room in rooms}
        self.character_order = characters
        self.character_dict = {game_character.character.get_name():game_character for game_character in characters}
        self.actions = actions
        
        i = 0
        for character in extra_characters:
            new_character = GameCharacter(character, start_rooms[i%len(start_rooms)], CommandLineController(), Inventory(10,10))
            self.character_dict[character.get_name()] = new_character
            self.character_order.append(new_character)
            i += 1
        self.current_turn = 0
        self.moves = 0

    def action(self, character:Character, action:Action, inputs:tuple) -> bool:
        self.current_turn += 1
        self.moves += 1

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
