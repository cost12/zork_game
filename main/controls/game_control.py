from typing import Any, Optional

from models.actors import Direction, Target, Actor, LocationDetail
from models.action import Action
from factories.factories import ItemFactory, NamedFactory, LocationFactory, CharacterFactory, CharacterControlFactory
from controls.character_control import CommandLineController, Feedback
from controls.translate import get_input_translator

# TODO: Target/actor/tool response should depend on Action, State, and success (of Action)
# Targets/tools might have requirements for being used -> State?
# TODO: responses should be their own class?
# TODO: need a way to place Items in LocationDetails
# TODO: handle multiple items with same name
# TODO: low priority: exit text when passing through an exit
# TODO: handle json input of bools correctly
# TODO: is hidden needed in LocationDetail? (replaced by hidden_when)
# TODO: for many items with same name: have unique id for equality/ dicts, dict[str,Named] -> dict[str,list[Named]] and figure out which one based on context/ asking questions

class GameAction:
    """This is an abstract class and should not be instantiated.
    Represents an Action a Character can make during a Game.
    Verifies the Action inputs and determines the results of the Action
    """

    def __init__(self, action:Action):
        """Creates a GameAction

        :param action: The Action that corresponds to this GameAction.
        The Action determines what words can be used to call this Action and how internal States of Characters and Items will be updated.
        :type action: Action
        """
        self.action = action

    def check_inputs(self, inputs:tuple) -> tuple[bool,tuple,Optional[str]]:
        """Verifies that the inputs to this GameAction are valid.

        :param inputs: The inputs to check
        :type inputs: tuple
        :return: A tuple describing if the inputs are valid, the reformatted inputs to be used (if valid), and a response
        :rtype: tuple[bool,tuple,Optional[str]]
        """
        pass

    def take_action(self, character:Actor, inputs) -> Feedback:
        """Performs the GameAction and modifies the Characters/Items accordingly. 
        Returns a summary of the resulst in Feedback

        :param character: The Character performing the GameAction
        :type character: Actor
        :param inputs: The inputs to the GameAction, including any targets or tools used
        :type inputs: Any
        :return: A summary of the result of the GameAction
        :rtype: Feedback
        """
        pass

    def __combine_responses__(self, responses:list[str|None]) -> str:
        """Combines responses from various sources into one readable string

        :param responses: Character/Item responses to different parts of a GameAction
        :type responses: list[str | None]
        :return: A readable string of the combined responses
        :rtype: str
        """
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

    def __verify_character__(self, character:Actor) -> tuple[bool,Optional[str]]:
        """Verifies that character can perform the requested GameAction.

        :param character: The Character attempting to perform a GameAction
        :type character: Actor
        :return: A bool that describes whether character can perform the GameAction and the character's response
        :rtype: tuple[bool,Optional[str]]
        """
        response = character.get_actor_response(self.action)
        if self.action in character.get_actions_as_actor():
            return True, response
        if response is None:
            response = f"You are unable to perform this action."
        return False, response

    def __verify_target__(self, character:Actor, target:Target) -> tuple[bool,str]:
        """Verifies that target can have the GameAction performed on it.

        :param character: The Character attempting to perform the GameAction
        :type character: Actor
        :param target: The Target character is attempting to target with this GameAction
        :type target: Target
        :return: A bool that describes whether target can have the GameAction performed on it and the target's response
        :rtype: tuple[bool,str]
        """
        room,_ = character.get_location()
        target_room, detail = target.get_location()
        if target_room == room:
            if not detail.is_hidden() or target in character.get_inventory_items():
                response = target.get_target_response(self.action)
                if self.action in target.get_actions_as_target():
                    return True, response
                if response is None:
                    response = f"The {target.get_name()} resists the action."
                return False, response
            return False, f"You can't seen any {target.get_name()} here."
        return False, f"There is no {target.get_name()} in this room."

    def __verify_tool__(self, character:Actor, tool:Target) -> tuple[bool,str]:
        """Verifies that tool can be used to perform this GameAction.

        :param character: The Character using the tool
        :type character: Actor
        :param tool: The tool used
        :type tool: Target
        :return: A bool that describes whether tool can be used by character to perform the GameAction and the tool's response
        :rtype: tuple[bool,str]
        """
        room,_ = character.get_location()
        tool_room, detail = tool.get_location()
        if tool_room == room:
            if not detail.is_hidden() or tool in character.get_inventory_items():
                response = tool.get_tool_response(self.action)
                if self.action in tool.get_actions_as_target():
                    return True, response
                if response is None:
                    response = f"The {tool.get_name()} can't be used in this way."
                return False, response
            return False, f"You can't see any {tool.get_name()} here."
        return False, f"There is no {tool.get_name()} in this room."
    
class LookAction(GameAction):
    """Inherits from GameAction.
    A GameAction that tells a Character what they see
    """

    def check_inputs(self, inputs) -> tuple[bool,tuple,Optional[str]]:
        if len(inputs) == 0:
            return True, inputs, None
        elif len(inputs) == 1:
            if isinstance(inputs[0], Target):
                return True, inputs, None
            return False, None, "You can't look at that."
        return False, None, "Pick something to focus on."
    
    def take_action(self, character:Actor, target:Optional[Target]=None) -> Feedback:
        response = []
        can_look, r = self.__verify_character__(character)
        response.append(r)
        if can_look:
            if target is None:
                location, _ = character.get_location()
                response.extend(character.perform_action_as_actor(self.action))
                response.append(location.get_description(character))
                return Feedback(self.__combine_responses__(response), turns=0)
            else:
                can_be_seen, r = self.__verify_target__(character, target)
                response.append(r)
                if can_be_seen:
                    response.extend(character.perform_action_as_actor(self.action))
                    response.extend(target.perform_action_as_target(self.action))
                    response.append(f"You see a {target.get_description()}.")
                    return Feedback(self.__combine_responses__(response), turns=0)
        return Feedback(self.__combine_responses__(response), success=False, turns=0)

class WalkAction(GameAction):
    """Inherits from GameAction
    A GameAction that allows a Character to move from one room to another
    """

    def check_inputs(self, inputs:tuple) -> tuple[bool,tuple,Optional[str]]:
        if len(inputs) == 1:
            if isinstance(inputs[0], Direction):
                return True, inputs, None
            return False, None, "What direction?"
        if len(inputs) == 0:
            return False, None, "What direction?"
        return False, None, "That's a lot of words. Which way do you want to go?"

    def take_action(self, character:Actor, direction:Direction) -> Feedback:
        response = []
        can_walk, r = self.__verify_character__(character)
        response.append(r)
        if can_walk:
            room, detail = character.get_location()
            exit, r = room.get_path(character, direction)
            if r is None and exit is None:
                r = f"There is nothing {direction.get_name()}."
            response.append(r)
            if exit is not None:
                can_pass, reason, r = exit.can_pass(character)
                if r is None and not can_pass:
                    r = "You are unable to exit."
                response.append(r)
                if can_pass:
                    character.change_location(exit.get_end(character))
                    response.extend(character.perform_action_as_actor(self.action))
                    response.append(LookAction(Action('look')).take_action(character).as_string())
                    return Feedback(self.__combine_responses__(response))
        return Feedback(self.__combine_responses__(response), success=False, turns=0)

class WaitAction(GameAction):
    """Inherits from GameAction
    A GameAction that allows a Character to let time pass without doing anything.
    """

    def check_inputs(self, inputs:tuple) -> tuple[bool,tuple,Optional[str]]:
        if len(inputs) == 0:
            return True, None, None
        return False, None, "Thats a lot of words. Do you want to wait?"

    def take_action(self, character:Actor):
        response = []
        can_wait, r = self.__verify_character__(character)
        response.append(r)
        if can_wait:
            response.extend(character.perform_action_as_actor(self.action))
            return Feedback(self.__combine_responses__(response))
        return Feedback(self.__combine_responses__(response), success=False, turns=0)

class TakeAction(GameAction):
    """Inherits from GameAction
    A GameAction that allows a Character to add an item (or items) to their Inventory
    """

    def check_inputs(self, inputs) -> tuple[bool,tuple,Optional[str]]:
        for input in inputs:
            if not isinstance(input, Target):
                return False, None, f"You can't take a {input.get_name()}!"
        if len(inputs) > 0:
            return True, (inputs,), None
        return False, None, "Take what?"
    
    def take_action(self, character:Actor, targets:list[Target]) -> Feedback:
        response = []
        can_take, r = self.__verify_character__(character)
        response.append(r)
        success = False
        if can_take:
            for target in targets:
                can_be_taken, target_response = self.__verify_target__(character, target)
                response.append(target_response)
                if can_be_taken:
                    if character.add_item_to_inventory(target):
                        success = True
                        response.extend(target.perform_action_as_target(self.action))
                    else:
                        response.append(f"The {target.get_name()} doesn't fit in your pack.")
                if success:
                    response.append("Taken.")
                    response.extend(character.perform_action_as_actor(self.action))
                else:
                    response.append("No items were taken.")
        return Feedback(self.__combine_responses__(response), success=success, turns=1 if success else 0)

class DropAction(GameAction):
    """Inherits from GameAction
    A GameAction that allows a Character to drop an item (or items) from their Inventory
    """

    def check_inputs(self, inputs) -> tuple[bool,tuple,Optional[str]]:
        for input in inputs:
            if not isinstance(input, Target):
                return False, None, f"You can't drop a {input.get_name()}!"
        if len(inputs) > 0:
            return True, (inputs,), None
        return False, None, "Drop what?"
    
    def take_action(self, character:Actor, targets:list[Target], placement:Optional[LocationDetail]) -> Feedback:
        response = []
        can_drop, r = self.__verify_character__(character)
        response.append(r)
        success = False
        if can_drop:
            for target in targets:
                can_be_dropped, target_response = self.__verify_target__(character, target)
                response.append(target_response)
                if can_be_dropped:
                    dropped, r = character.remove_item_from_inventory(target, placement)
                    response.extend(r)
                    if dropped:
                        success = True
                        response.extend(target.perform_action_as_target(self.action))
                    else:
                        response.append(f"You aren't holding a {target.get_name()}.")
                if success:
                    response.append("Dropped.")
                    response.extend(character.perform_action_as_actor(self.action))
                else:
                    response.append("No items were dropped.")
        return Feedback(self.__combine_responses__(response), success=success, turns=1 if success else 0)

class CheckInventoryAction(GameAction):
    """Inherits from GameAction
    A GameAction that allows a Character to view the contents of their Inventory
    """

    def check_inputs(self, inputs:tuple) -> tuple[bool,tuple,Optional[str]]:
        if len(inputs) == 0:
            return True, None, None
        return False, None, f"That's a lot of words."
    
    def take_action(self, character:Actor) -> Feedback:
        response = []
        can_check, r = self.__verify_character__(character)
        response.append(r)
        if can_check:
            if len(character.get_inventory_items()) > 0:
                r = "Your inventory contains:\n\t"
                r += "\n\t".join([item.get_name() for item in character.get_inventory_items()])
            else:
                r = "Your inventory is empty."
            response.append(r)
            return Feedback(self.__combine_responses__(response), turns=0)
        return Feedback(self.__combine_responses__(response), success=False, turns=0)

class DefaultAction(GameAction):
    """Inherits from GameAction
    A default GameAction that updates Character/Target states but has no other effect
    """

    def check_inputs(self, inputs:tuple) -> tuple[bool,tuple,str]:
        return True, (inputs,), None
    
    def take_action(self, character:Actor, inputs:tuple[Target]) -> Feedback:
        response = ["This action is not implemented and may result in errors."]
        can_act, r = self.__verify_character__(character)
        response.append(r)
        success = False
        if can_act:
            for target in inputs:
                can_take_act, target_response = self.__verify_target__(character, target)
                response.append(target_response)
                if can_take_act:
                    success = True
                    response.extend(target.perform_action_as_target(self.action))
            if success:
                response.extend(character.perform_action_as_actor(self.action))
        return Feedback(self.__combine_responses__(response), success=success, turns=0)

class GameState:
    """Represents an instance of a Zork game
    """

    def __init__(self, details:dict[str,Any], rooms:LocationFactory, characters:CharacterFactory, extra_characters:list[Actor], controllers:CharacterControlFactory, actions:NamedFactory[Action], items:ItemFactory, directions:NamedFactory[Direction]):
        """Creates a GameState

        :param details: Any details not captured in the other inputs. Includes the welcome text
        :type details: dict[str,Any]
        :param rooms: All the Rooms in the game
        :type rooms: LocationFactory
        :param characters: All the Characters in the game
        :type characters: CharacterFactory
        :param extra_characters: If there are more users than default playable Characters (and the game allows it) these are additional user created and controlled Characters.
        :type extra_characters: list[Actor]
        :param controllers: A factory that determines how Characters in the game will be controlled (user input vs cpu controlled)
        :type controllers: CharacterControlFactory
        :param actions: All the Actions that can be taken in the game
        :type actions: NamedFactory[Action]
        :param items: All the Items in the game
        :type items: ItemFactory
        :param directions: All the directions in the game
        :type directions: NamedFactory[Direction]
        """
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
            self.actions.get_named('look'): LookAction(self.actions.get_named('look')),
            self.actions.get_named('walk'): WalkAction(self.actions.get_named('walk')),
            self.actions.get_named('wait'): WaitAction(self.actions.get_named('wait')),
            self.actions.get_named('take'): TakeAction(self.actions.get_named('take')),
            self.actions.get_named('drop'): DropAction(self.actions.get_named('drop')),
            self.actions.get_named('inventory'):CheckInventoryAction(self.actions.get_named('inventory')),
        })
        self.default_action = DefaultAction(self.actions.get_named('look'))
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
        """Determines which Character makes the next Action

        :return: The Character whose turn it is
        :rtype: Actor
        """
        return self.character_order[self.current_turn%len(self.character_order)]

    def game_over(self) -> bool:
        """Determines when the game is over

        :return: Whether the game is over or not
        :rtype: bool
        """
        pass

    def translate(self, user_input:str) -> tuple[Action,list]:
        """Translates user input into a GameAction

        :param user_input: Input from a Character. Can be any string
        :type user_input: str
        :return: A GameAction and its inputs or an error message
        :rtype: tuple[Action,list]
        """
        return self.translator.interpret(user_input, self.actions.aliases, self.characters.aliases, self.rooms.aliases, self.items.aliases, self.directions.aliases)
    
    ###########################################################################
    # Main driver
    ###########################################################################
    def play(self) -> None:
        """Driving function to advance GameState.
        Prompts Characters for input on their turn and performs the GameActions until the game is over
        """
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
        """Mutates the GameState by completing the specified Action

        :param character: The Character to perform the action
        :type character: Actor
        :param action: The Action to be performed
        :type action: Action
        :param inputs: The inputs to the Action
        :type inputs: tuple
        :return: Notable results of the Action
        :rtype: Feedback
        """
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
