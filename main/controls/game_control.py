from typing import Any, Optional

from models.actors              import Target, Actor, Location, LocationDetail
from models.named               import Action, Direction
from factories.factories        import CharacterControlFactory
from models.response            import ResponseString, Response, CombinationResponse, StaticResponse, ContentsResponse, BackupResponse
from controls.character_control import CommandLineController, Feedback, CharacterController
from controls.translate         import get_input_translator
from utils.constants            import *
from utils.relator              import NameFinder
from models.requirement         import ActionRequirement

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

    def check_inputs(self, inputs:tuple) -> tuple[bool,tuple,ResponseString]:
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

    def __combine_responses__(self, responses:list[str|None]) -> ResponseString:
        """Combines responses from various sources into one readable string

        :param responses: Character/Item responses to different parts of a GameAction
        :type responses: list[str | None]
        :return: A readable string of the combined responses
        :rtype: ResponseString
        """
        return CombinationResponse(responses=[response for response in responses if response is not None], joiner="\n")

    def __verify_character__(self, character:Actor, *, action:Action=None) -> tuple[bool,ResponseString]:
        """Verifies that character can perform the requested GameAction.

        :param character: The Character attempting to perform a GameAction
        :type character: Actor
        :return: A bool that describes whether character can perform the GameAction and the character's response
        :rtype: tuple[bool,Optional[str]]
        """
        if action is None:
            action = self.action
        response = character.get_actor_response(action)
        r2 = None
        if action in character.get_actions_as_actor():
            room = character.get_top_parent()
            assert isinstance(room, Location)
            allowed, r2 = room.action_allowed(character, action)
            if allowed:
                return True, response
        return False, BackupResponse([response, r2, StaticResponse("You are unable to perform this action.")])

    def __verify_target__(self, character:Actor, target:Target) -> tuple[bool,ResponseString]:
        """Verifies that target can have the GameAction performed on it.

        :param character: The Character attempting to perform the GameAction
        :type character: Actor
        :param target: The Target character is attempting to target with this GameAction
        :type target: Target
        :return: A bool that describes whether target can have the GameAction performed on it and the target's response
        :rtype: tuple[bool,str]
        """
        room = character.get_top_parent()
        assert isinstance(room, Location)
        if room.can_interact_with(character, target):
            response = target.get_target_response(self.action)
            if self.action in target.get_actions_as_target():
                return True, response
            return False, BackupResponse([response, StaticResponse(f"The {target.get_name()} resists the action.")])
        return False, StaticResponse(f"There is no {target.get_name()} in this room.")

    def __verify_tool__(self, character:Actor, tool:Target) -> tuple[bool,ResponseString]:
        """Verifies that tool can be used to perform this GameAction.

        :param character: The Character using the tool
        :type character: Actor
        :param tool: The tool used
        :type tool: Target
        :return: A bool that describes whether tool can be used by character to perform the GameAction and the tool's response
        :rtype: tuple[bool,str]
        """
        room = character.get_top_parent()
        assert isinstance(room, Location)
        if room.can_interact_with(character, tool):
            response = tool.get_tool_response(self.action)
            if self.action in tool.get_actions_as_target():
                return True, response
            return False, BackupResponse([response, StaticResponse(f"The {tool.get_name()} can't be used in this way.")])
        return False, StaticResponse(f"There is no {tool.get_name()} in this room.")
    
class LookAction(GameAction):
    """Inherits from GameAction.
    A GameAction that tells a Character what they see
    """

    def check_inputs(self, inputs) -> tuple[bool,tuple,ResponseString]:
        if len(inputs) == 0:
            return True, inputs, None
        elif len(inputs) == 1:
            if isinstance(inputs[0], Target):
                return True, inputs, None
            return False, None, StaticResponse("You can't look at that.")
        return False, None, StaticResponse("Pick something to focus on.")
    
    def take_action(self, character:Actor, target:Optional[Target]=None) -> Feedback:
        response = []
        can_look, r = self.__verify_character__(character)
        response.append(r)
        if can_look:
            if target is None:
                location = character.get_top_parent()
                if not isinstance(location, Location):
                    print(location)
                    print(type(location))
                response.append(character.perform_action_as_actor(self.action))
                response.append(location.get_description_to(character))
                return Feedback(self.__combine_responses__(response), Response(character, self.action, True), turns=0)
            else:
                can_be_seen, r = self.__verify_target__(character, target)
                response.append(r)
                if can_be_seen:
                    response.append(character.perform_action_as_actor(self.action))
                    response.append(target.perform_action_as_target(self.action))
                    response.append(target.get_description_to(character))
                    return Feedback(self.__combine_responses__(response), Response(character, self.action, True, target=target), turns=0)
        return Feedback(self.__combine_responses__(response), Response(character, self.action, success=False, target=target), turns=0)

class WalkAction(GameAction):
    """Inherits from GameAction
    A GameAction that allows a Character to move from one room to another
    """

    def check_inputs(self, inputs:tuple) -> tuple[bool,tuple,ResponseString]:
        if len(inputs) == 1:
            if isinstance(inputs[0], Direction):
                return True, inputs, None
            return False, None, StaticResponse("What direction?")
        if len(inputs) == 0:
            return False, None, StaticResponse("What direction?")
        return False, None, StaticResponse("That's a lot of words. Which way do you want to go?")

    def take_action(self, character:Actor, direction:Direction) -> Feedback:
        response = []
        can_walk, r = self.__verify_character__(character)
        can_see, _ = self.__verify_character__(character, action=Action("look"))
        if not can_see:
            response.append(StaticResponse("You fumble around in the darkness blindly, finally finding an exit."))
            direction = Direction("random")
        response.append(r)
        if can_walk:
            room = character.get_top_parent()
            assert isinstance(room, Location)
            exit, r = room.get_path(character, direction)
            if exit is None:
                if direction.get_name() == 'random':
                    response.append(BackupResponse([r, StaticResponse(f"Unfortunately you can't seem to exit through the path you've found. Maybe try again.")]))
                else:
                    response.append(BackupResponse([r, StaticResponse(f"There is nothing {direction.get_name()}.")]))
            else:
                response.append(r)
                can_pass, r = exit.can_pass(character)
                if can_pass:
                    response.append(r)
                    character.set_location(exit.get_end(character))
                    response.append(character.perform_action_as_actor(self.action))
                    response.append(LookAction(Action('look')).take_action(character).response_string)
                    return Feedback(self.__combine_responses__(response), Response(character, self.action, True))
                else:
                    response.append(BackupResponse([r, StaticResponse("You are unable to exit.")]))
        return Feedback(self.__combine_responses__(response), Response(character, self.action, False), turns=0)

class WaitAction(GameAction):
    """Inherits from GameAction
    A GameAction that allows a Character to let time pass without doing anything.
    """

    def check_inputs(self, inputs:tuple) -> tuple[bool,tuple,ResponseString]:
        if len(inputs) == 0:
            return True, None, None
        return False, None, StaticResponse("Thats a lot of words. Do you want to wait?")

    def take_action(self, character:Actor):
        response = []
        can_wait, r = self.__verify_character__(character)
        response.append(r)
        if can_wait:
            response.append(BackupResponse([character.perform_action_as_actor(self.action), StaticResponse("Time passes.")]))
            return Feedback(self.__combine_responses__(response), Response(character, self.action, True))
        return Feedback(self.__combine_responses__(response), Response(character, self.action, False), turns=0)

class TakeAction(GameAction):
    """Inherits from GameAction
    A GameAction that allows a Character to add an item (or items) to their Inventory
    """

    def check_inputs(self, inputs) -> tuple[bool,tuple,ResponseString]:
        for input in inputs:
            if not isinstance(input, Target):
                return False, None, StaticResponse(f"You can't take a {input.get_name()}!")
        if len(inputs) > 0:
            return True, (inputs,), None
        return False, None, StaticResponse("Take what?")
    
    def take_action(self, character:Actor, targets:list[Target]) -> Feedback:
        response = []
        can_take, r = self.__verify_character__(character)
        response.append(r)
        success = False
        target=None
        if can_take:
            for target in targets:
                can_be_taken, target_response = self.__verify_target__(character, target)
                if DEBUG_TAKE: print(f"Take {target}? {can_be_taken}")
                response.append(target_response)
                if can_be_taken:
                    added, r = character.add_to_inventory(target)
                    response.append(r)
                    if added:
                        success = True
                        response.append(target.perform_action_as_target(self.action))
                    else:
                        response.append(StaticResponse(f"The {target.get_name()} doesn't fit in your pack."))
            if success:
                response.append(StaticResponse("Taken."))
                response.append(character.perform_action_as_actor(self.action))
            else:
                response.append(StaticResponse("No items were taken."))
        return Feedback(self.__combine_responses__(response), Response(character, self.action, success, target=target), turns=1 if success else 0)

class DropAction(GameAction):
    """Inherits from GameAction
    A GameAction that allows a Character to drop an item (or items) from their Inventory
    """

    def check_inputs(self, inputs) -> tuple[bool,tuple,ResponseString]:
        targets = []
        placement = None
        for input in inputs:
            if isinstance(input, Target):
                targets.append(input)
            elif isinstance(input, tuple) and input[0] == 'placement':
                placement = input[1]
            else:
                return False, None, StaticResponse(f"You can't drop a {input.get_name()}!")
        if len(inputs) > 0:
            return True, (targets,placement), None
        return False, None, StaticResponse("Drop what?")
    
    def take_action(self, character:Actor, targets:list[Target], placement:Optional[LocationDetail]=None) -> Feedback:
        response = []
        can_drop, r = self.__verify_character__(character)
        response.append(r)
        success = False
        target=None
        if can_drop:
            for target in targets:
                can_be_dropped, target_response = self.__verify_target__(character, target)
                response.append(target_response)
                if can_be_dropped:
                    room = character.get_top_parent()
                    assert isinstance(room, Location)
                    if placement is None or room.can_interact_with(character, placement):
                        dropped, r = character.remove_from_inventory(target, placement)
                        response.append(r)
                        if dropped:
                            success = True
                            response.append(target.perform_action_as_target(self.action))
                    else:
                        response.append(StaticResponse(f"There is no {placement.get_name()} here."))
            if success:
                response.append(StaticResponse("Dropped."))
                response.append(character.perform_action_as_actor(self.action))
            else:
                response.append(StaticResponse("No items were dropped."))
        return Feedback(self.__combine_responses__(response), Response(character, self.action, success=success, target=target), turns=1 if success else 0)

class CheckInventoryAction(GameAction):
    """Inherits from GameAction
    A GameAction that allows a Character to view the contents of their Inventory
    """

    def check_inputs(self, inputs:tuple) -> tuple[bool,tuple,ResponseString]:
        if len(inputs) == 0:
            return True, None, None
        return False, None, StaticResponse(f"That's a lot of words.")
    
    def take_action(self, character:Actor) -> Feedback:
        response = []
        can_check, r = self.__verify_character__(character)
        response.append(r)
        if can_check:
            response.append(ContentsResponse(StaticResponse("Your inventory contains:\n\t"), StaticResponse("Your inventory is empty."), character, inventory=True))
            return Feedback(self.__combine_responses__(response), Response(character, self.action, True), turns=0)
        return Feedback(self.__combine_responses__(response), Response(character, self.action, False), turns=0)

class DefaultAction(GameAction):
    """Inherits from GameAction
    A default GameAction that updates Character/Target states but has no other effect
    """

    def check_inputs(self, inputs:tuple) -> tuple[bool,tuple,str]:
        return True, (inputs,), None
    
    def take_action(self, character:Actor, inputs:tuple[Target]) -> Feedback:
        response = list[ResponseString]()
        if not self.action.use_default():
            response = [StaticResponse("This action is not implemented and may result in errors.")]
        can_act, r = self.__verify_character__(character)
        response.append(r)
        success = False
        target=None
        if can_act:
            for target in inputs:
                can_take_act, target_response = self.__verify_target__(character, target)
                response.append(target_response)
                if can_take_act:
                    success = True
                    response.append(target.perform_action_as_target(self.action))
            if success:
                response.append(character.perform_action_as_actor(self.action))
        response = BackupResponse([self.__combine_responses__(response), StaticResponse("Success." if success else "Fail.")])
        return Feedback(response, Response(character, self.action, success=success, target=target), turns=0)

class GameState:
    """Represents an instance of a Zork game
    """

    def __init__(self, details:dict[str,Any], name_space:NameFinder, extra_characters:list[Actor], controllers:CharacterControlFactory, every_turn_requirement:list[ActionRequirement]):
        self.game_details    = details
        self.name_space      = name_space
        self.character_order:list[Actor] = self.name_space.get_from_name(category='actor')
        self.controllers     = controllers
        self.every_turn_requirement = every_turn_requirement
        self.translator      = get_input_translator()
        self.current_turn    = 0
        self.moves           = 0
        self.action_dict     = dict[Action,GameAction]({
            self.name_space.get_from_name('look', 'action')[0]: LookAction(self.name_space.get_from_name('look', 'action')[0]),
            self.name_space.get_from_name('walk', 'action')[0]: WalkAction(self.name_space.get_from_name('walk', 'action')[0]),
            self.name_space.get_from_name('wait', 'action')[0]: WaitAction(self.name_space.get_from_name('wait', 'action')[0]),
            self.name_space.get_from_name('take', 'action')[0]: TakeAction(self.name_space.get_from_name('take', 'action')[0]),
            self.name_space.get_from_name('drop', 'action')[0]: DropAction(self.name_space.get_from_name('drop', 'action')[0]),
            self.name_space.get_from_name('inventory', 'action')[0]:CheckInventoryAction(self.name_space.get_from_name('inventory', 'action')[0]),
        })
        self.default_action = DefaultAction(self.name_space.get_from_name('look', 'action'))
        i = 0
        start_rooms = [room for room in self.name_space.get_from_name(category='location') if room.is_start_location()]
        for character in extra_characters:
            start_room = start_rooms[i%len(start_rooms)]
            controllers.create_character(character, CommandLineController())
            character.set_location(start_room, origin=True)
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

    def translate(self, user_input:str, character:Actor, controller:CharacterController) -> tuple[Action,list]:
        """Translates user input into a GameAction

        :param user_input: Input from a Character. Can be any string
        :type user_input: str
        :param character: The character making the input
        :type character: Actor
        :param controller: The controller for the character making the input, for clarifications
        :type controller: CharacterController
        :return: A GameAction and its inputs or an error message
        :rtype: tuple[Action,list]
        """
        return self.translator.interpret(user_input, self.name_space, character, controller)
    
    ###########################################################################
    # Main driver
    ###########################################################################
    def play(self) -> None:
        """Driving function to advance GameState.
        Prompts Characters for input on their turn and performs the GameActions until the game is over
        """
        print(f"{self.game_details["welcome_text"]}\n")
        # Initial look for all characters
        for character in self.character_order:
            controller = self.controllers.get_controller(character)
            feedback = self.action(character, self.name_space.get_from_name('look','action')[0], tuple())
            controller.feedback(feedback)
        while not self.game_over():
            # Check/update requirements that need to be checked every turn
            for character in self.character_order:
                for requirement in self.every_turn_requirement:
                    requirement._check_every_turn(character)
            # do the turn
            character = self.whose_turn()
            controller = self.controllers.get_controller(character)
            user_input = controller.make_move()
            action, inputs = self.translate(user_input, character, controller)
            if DEBUG_INPUT:
                print(f"{character}: {action} {inputs}")
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
            feedback = Feedback(StaticResponse(inputs.message), Response(character, action, False), turns=0)
        elif action in self.action_dict:
            valid, inputs, response = self.action_dict[action].check_inputs(inputs)
            if valid:
                if inputs is not None:
                    feedback = self.action_dict[action].take_action(character, *inputs)
                else:
                    feedback = self.action_dict[action].take_action(character)
            else:
                feedback = Feedback(response, Response(character, action, False), turns=0)
        else:
            self.default_action.action = action
            valid, inputs, response = self.default_action.check_inputs(inputs)
            if valid:
                if inputs is not None:
                    feedback = self.default_action.take_action(character, *inputs)
                else:
                    feedback = self.default_action.take_action(character)
            else:
                feedback = Feedback(response, Response(character, action, False), turns=0)
        self.current_turn += feedback.turns
        self.moves += feedback.moves
        return feedback
