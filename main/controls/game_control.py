from typing import Any, Optional

from models.actors import Direction, Target, Actor, Location
from models.action import Action
from factories.factories import ItemFactory, NamedFactory, StateFactory, LocationFactory, SkillSetFactory, CharacterFactory, StateGraphFactory, LocationDetailFactory, CharacterControlFactory, StateDisconnectedGraphFactory
from controls.character_control import CommandLineController, Feedback
from controls.translate import get_input_translator

# Where do target/actor/tool responses go?
# What if the action is/isn't successful?
# Targets/tools might have requirements for being used

class GameAction:

    def __init__(self, action:Action):
        self.action = action

    def check_inputs(self, inputs:tuple) -> tuple[bool,tuple,str]:
        pass

    def take_action(self, character:Actor, inputs) -> Feedback:
        pass

    def __combine_responses__(self, responses:list[str|None]) -> str:
        result = ""
        first = True
        for response in responses:
            if response is None or response == "":
                continue
            if not first:
                result += "\n"
            result += response
            first = False
        return result

    def __verify_character__(self, character:Actor) -> tuple[bool,str]:
        if self.action in character.get_actions_as_actor():
            return True, ''
        return False, f"You are unable to perform this action."

    def __verify_target__(self, character:Actor, target:Target) -> tuple[bool,str]:
        room,_ = character.get_location()
        target_room, detail = target.get_location()
        if target_room == room:
            if not detail.is_hidden() or target in character.get_inventory_items():
                if self.action in target.get_actions_as_target():
                    return True, ""
                return False, f"The {target.get_name()} resists the action."
            return False, f"You can't seen any {target.get_name()} here."
        return False, f"There is no {target.get_name()} in this room."

    def __verify_tool__(self, character:Actor, tool:Target) -> tuple[bool,str]:
        room,_ = character.get_location()
        tool_room, detail = tool.get_location()
        if tool_room == room:
            if not detail.is_hidden() or tool in character.get_inventory_items():
                if self.action in tool.get_actions_as_target():
                    return True, ""
                return False, f"The {tool.get_name()} can't be used in this way."
            return False, f"You can't seen any {tool.get_name()} here."
        return False, f"There is no {tool.get_name()} in this room."
    
class LookAction(GameAction):
    def check_inputs(self, inputs) -> tuple[bool,tuple,str]:
        if len(inputs) == 0:
            return True, inputs, ""
        elif len(inputs) == 1:
            if isinstance(inputs[0], Target):
                return True, inputs, ""
            return False, None, "You can't look at that."
        return False, None, "Pick something to focus on."
    
    def take_action(self, character:Actor, target:Optional[Target]=None) -> Feedback:
        can_look, response = self.__verify_character__(character)
        if can_look:
            if target is None:
                location, _ = character.get_location()
                response1 = character.perform_action_as_actor(self.action)
                response = self.__combine_responses__([*response1, location.get_description(character)])
                return Feedback(response, turns=0)
            else:
                can_be_seen, response = self.__verify_target__(character, target)
                if can_be_seen:
                    response = character.perform_action_as_actor(self.action)
                    response.extend(target.perform_action_as_target(self.action))
                    response = self.__combine_responses__([*response, target.get_description()])
                    return Feedback(response)
        return Feedback(response, success=False, turns=0)

class WalkAction(GameAction):

    def check_inputs(self, inputs:tuple) -> tuple[bool,tuple,str]:
        if len(inputs) == 1:
            if isinstance(inputs[0], Direction):
                return True, inputs, ""
            return False, None, "What direction?"
        if len(inputs) == 0:
            return False, None, "What direction?"
        return False, None, "That's a lot of words. Which way do you want to go?"

    def take_action(self, character:Actor, direction:Direction) -> Feedback:
        can_walk, response = self.__verify_character__(character)
        if can_walk:
            room, detail = character.get_location()
            exit, response = room.get_path(direction)
            if exit is not None:
                can_pass, reason, response = exit.can_pass(character)
                if can_pass:
                    character.change_location(exit.get_end())
                    response2 = character.perform_action_as_actor(self.action)
                    response3 = LookAction(Action('look')).take_action(character).as_string()
                    responses = [response, *response2, response3]
                    response = self.__combine_responses__(responses)
                    return Feedback(response)
                elif response is None:
                    response = "You are unable to exit."
            elif response is None:
                response = f"There is nothing {direction.get_name()}."
        return Feedback(response, success=False, turns=0)

class WaitAction(GameAction):

    def check_inputs(self, inputs:tuple) -> tuple[bool,tuple,str]:
        if len(inputs) == 0:
            return True, None, ""
        return False, None, "Thats a lot of words. Do you want to wait?"

    def take_action(self, character:Actor):
        can_wait, response = self.__verify_character__(character)
        if can_wait:
            responses = character.perform_action_as_actor(self.action)
            response = self.__combine_responses__(responses)
            return Feedback(response)
        return Feedback(response, success=False, turns=0)

class TakeAction(GameAction):
    # How will inputs be formatted correctly?

    def check_inputs(self, inputs) -> tuple[bool,tuple,str]:
        for input in inputs:
            if not isinstance(input, Target):
                return False, None, f"You can't take a {input.get_name()}!"
        if len(inputs) > 0:
            return True, (inputs,), ""
        return False, None, "Take what?"
    
    def take_action(self, character:Actor, targets:list[Target]) -> Feedback:
        can_take, response = self.__verify_character__(character)
        success = False
        if can_take:
            response = ""
            for target in targets:
                can_be_taken, target_response = self.__verify_target__(character, target)
                response = self.__combine_responses__([response, target_response])
                if can_be_taken:
                    if character.add_item_to_inventory(target):
                        success = True
                        target_responses = target.perform_action_as_target(self.action)
                        response = self.__combine_responses__([response, *target_responses])
                    else:
                        response = self.__combine_responses__([response, f"The {target.get_name()} didn't fit in your pack."])
                if success:
                    character_responses = character.perform_action_as_actor(self.action)
                    response = self.__combine_responses__([response, "Taken.", *character_responses])
        return Feedback(response, success=success, turns=0)

class CheckInventoryAction(GameAction):

    def check_inputs(self, inputs:tuple) -> tuple[bool,tuple,str]:
        if len(inputs) == 0:
            return True, None, ""
        return False, None, f"That's a lot of words."
    
    def take_action(self, character:Actor) -> Feedback:
        can_check, response = self.__verify_character__(character)
        if can_check:
            response = "Your inventory contains:\n\t"
            response += "\n\t".join([item.get_name() for item in character.get_inventory_items()])
            return Feedback(response, turns=0)
        return Feedback(response, success=False, turns=0)

class DefaultAction(GameAction):

    def check_inputs(self, inputs:tuple) -> tuple[bool,tuple,str]:
        return True, (inputs,), ""
    
    def take_action(self, character:Actor, inputs:tuple[Target]) -> Feedback:
        can_act, response = self.__verify_character__(character)
        success = False
        if can_act:
            for target in inputs:
                can_take_act, target_response = self.__verify_target__(character, target)
                response = self.__combine_responses__([response,target_response])
                if can_take_act:
                    success = True
                    target_responses = target.perform_action_as_target(self.action)
                    response = self.__combine_responses__([response, *target_responses])
            if success:
                responses = character.perform_action_as_actor(self.action)
                response = self.__combine_responses__([response, *responses])
        return Feedback(response, success=success,turns=0)

class GameState:

    def __init__(self, details:dict[str,Any], rooms:LocationFactory, characters:CharacterFactory, extra_characters:list[Actor], controllers:CharacterControlFactory, actions:NamedFactory[Action], items:ItemFactory, directions:NamedFactory[Direction]):
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
        self.action_dict     = dict[Action,GameAction]({
            self.actions.get_named('walk'): WalkAction(self.actions.get_named('walk')),
            self.actions.get_named('look'): LookAction(self.actions.get_named('look')),
            self.actions.get_named('wait'): WaitAction(self.actions.get_named('wait')),
            self.actions.get_named('take'): TakeAction(self.actions.get_named('take')),
            self.actions.get_named('inventory'):CheckInventoryAction(self.actions.get_named('inventory')),
        })
        self.default_action = DefaultAction(self.actions.get_named('walk'))
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
    def whose_turn(self) -> Actor:
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
            user_input = controller.make_move()
            action, inputs = self.translate(user_input)
            feedback = self.action(character, action, inputs)
            controller.feedback(feedback)

    ###########################################################################
    # Actions
    ###########################################################################
    def action(self, character:Actor, action:Action, inputs:tuple) -> Feedback:
        feedback = None
        if action == 'error':
            feedback = Feedback(inputs.message,success=False,turns=0)
        elif action in self.action_dict:
            valid, inputs, response = self.action_dict[action].check_inputs(inputs)
            if valid:
                if inputs is not None:
                    feedback = self.action_dict[action].take_action(character, *inputs)
                else:
                    feedback = self.action_dict[action].take_action(character)
            else:
                feedback = Feedback(response, success=False, turns=0)
        else:
            self.default_action.action = action
            valid, inputs, response = self.default_action.check_inputs(inputs)
            if valid:
                if inputs is not None:
                    feedback = self.default_action.take_action(character, *inputs)
                else:
                    feedback = self.default_action.take_action(character)
            else:
                feedback = Feedback(response, success=False, turns=0)
        self.current_turn += feedback.turns
        self.moves += feedback.moves
        return feedback
