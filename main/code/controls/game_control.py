from typing import Any, Optional

from code.models.character import Character
from code.models.item import Item
from code.models.actors import Direction, Target
from code.models.action import Action
from code.factories.factories import ItemFactory, NamedFactory, StateFactory, LocationFactory, SkillSetFactory, CharacterFactory, StateGraphFactory, LocationDetailFactory, CharacterControlFactory, StateDisconnectedGraphFactory
from code.controls.character_control import CommandLineController, Feedback
from code.controls.translate import get_input_translator

class GameState:

    def __init__(self, details:dict[str,Any], rooms:LocationFactory, characters:CharacterFactory, extra_characters:list[Character], controllers:CharacterControlFactory, actions:NamedFactory[Action], items:ItemFactory, directions:NamedFactory[Direction]):
        self.game_details    = details
        self.rooms           = rooms
        self.characters      = characters
        self.character_order = self.characters.get_characters()
        self.controllers     = controllers
        self.actions         = actions
        self.items           = items
        self.directions      = directions
        self.translator      = get_input_translator()
        self.current_turn    = 0
        self.moves           = 0
        #print(rooms.get_locations()[0])
        i = 0
        start_rooms = [room for room in rooms.get_locations() if room.is_start_location()]
        for character in extra_characters:
            start_room = start_rooms[i%len(start_rooms)]
            controllers.create_character(character, CommandLineController())
            character.change_location(start_room)
            character.origin = start_room
            i += 1
        
    ##########################################################################
    # Getters
    ##########################################################################
    def whose_turn(self) -> Character:
        return self.character_order[self.current_turn%len(self.character_order)]

    def game_over(self) -> bool:
        pass

    def translate(self, user_input:str) -> tuple[Action,list]:
        return self.translator.interpret(user_input, self.actions.aliases, self.characters.aliases, self.rooms.aliases, self.items.aliases, self.directions.aliases)
    
    ###########################################################################
    # Main driver
    ###########################################################################
    def play(self) -> None:
        print(self.game_details["welcome_text"])
        while not self.game_over():
            character = self.whose_turn()
            controller = self.controllers.get_controller(character)
            #print(character)
            user_input = controller.make_move()
            #print(f"Input: {user_input}")
            action, inputs = self.translate(user_input)
            #print(f"Translation: {action} {inputs}")
            feedback = self.action(character, action, inputs)
            #print(f"Feedback: {feedback}")
            controller.feedback(feedback)

    ###########################################################################
    # Actions
    ###########################################################################
    def action(self, character:Character, action:Action, inputs:tuple) -> Feedback:
        feedback = None
        if action == 'error':
            feedback = Feedback(inputs.message,success=False,turns=0)
        elif 'walk' in action.get_aliases():
            feedback = self.walk(character, inputs[0])
        elif 'look' in action.get_aliases():
            if len(inputs) > 0:
                feedback = self.look(character, inputs[0])
            else:
                feedback = self.look(character)
        elif 'wait' in action.get_aliases():
            feedback = Feedback("Time passes.")
            character.perform_action_as_actor(action)
        elif 'take' in action.get_aliases():
            feedback = self.take(character, inputs[0])
        elif "inventory" in action.get_aliases():
            feedback = self.check_inventory(character)
        else:
            feedback = Feedback("This has not been implemented yet.",turns=0)
            character.perform_action_as_actor(action)
            for input in inputs:
                if isinstance(input, Target):
                    input.perform_action_as_target(action)
        self.current_turn += feedback.turns
        self.moves += feedback.moves
        return feedback

    def walk(self, character:Character, direction:Direction) -> Feedback:
        room,detail = character.get_location()
        exit,response = room.get_path(direction)
        if exit is None:
            if response is None:
                return Feedback(f"There is nothing {direction.get_name()}.", turns=0, success=False)
            else:
                return Feedback(response, turns=0, success=False)
        can_pass,reason,path_response = exit.can_pass(character)
        if can_pass:
            character.change_location(exit.get_end())
            feedback_str = self.look(character).as_string()
            character.perform_action_as_actor(self.actions.get_named('walk'))
            if path_response is not None:
                feedback_str += f"\n{path_response}"
            feedback = Feedback(feedback_str)
            return feedback
        else:
            feedback_str = "You are unable to exit."
            if path_response is not None:
                feedback_str = path_response
            return Feedback(feedback_str, turns=0, success=False)
        
    def look(self, character:Character, target:Optional[Item]=None) -> Feedback:
        if target is None:
            location,_ = character.get_location()
            response = character.perform_action_as_actor(self.actions.get_named('look'))
            return Feedback(".".join(response) + location.get_description(character), turns=0)
        else:
            is_holding = character.is_holding(target)
            in_room,detail=character.get_location()[0].contains(target)
            hidden = detail.is_hidden()
            if is_holding or (in_room and not hidden):
                response = character.perform_action_as_actor(self.actions.get_named('look'))
                response.extend(target.perform_action_as_target(self.actions('look')))
                return Feedback(".".join(response) + target.get_description())
            else:
                return Feedback(f"There is no {target.get_name()} here.")
            
    def take(self, character:Character, target:Item) -> Feedback:
        action = self.actions.get_named('take')
        if action in character.get_actions_as_actor() and action in target.get_actions_as_target():
            location,_ = character.get_location()
            in_view,detail = location.contains(target)
            if (in_view and not detail.hidden) or target in character.get_inventory_items():
                if character.add_item_to_inventory(target):
                    response = character.perform_action_as_actor(action)
                    response.extend(target.perform_action_as_target(action))
                    if len(response) > 0:
                        return Feedback(f"{".".join(response)}. Taken.")
                    return Feedback("Taken.")
                else:
                    return Feedback(f"It doesn't seem to fit in your pack.", turns=0)
            return Feedback(f"There doesn't seem to be a {target.get_name()} here.", turns=0)
        return Feedback(f"Unfortunately you are unable to take the {target.get_name()}.", turns=0)
    
    def check_inventory(self, character:Character) -> Feedback:
        action = self.actions.get_named('inventory')
        if action in character.get_actions_as_actor():
            response = "Your inventory contains:\n"
            response += "\n".join([item.get_name() for item in character.get_inventory_items()])
            return Feedback(response, turns=0)
        return Feedback("You are unable to check your inventory.", turns=0)