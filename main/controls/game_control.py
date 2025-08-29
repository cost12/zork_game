from typing import Any

from models.actors              import Actor
from models.named               import Action
from factories.factories        import CharacterControlFactory
from controls.character_control import CommandLineController, Feedback, CharacterController
from controls.translate         import get_input_translator
from controls.actions           import GameAction
from utils.relator              import NameFinder
from controls.actions           import LookAction, WalkAction, WaitAction, TakeAction, DropAction, CheckInventoryAction, DefaultAction
from readin.restriction_helpers import Restriction
from readin.description_helpers import Description, plain_text_description
from utils.constants            import DEBUG_INPUT
class GameState:
    """Represents an instance of a Zork game
    """

    def __init__(self, details:dict[str,Any], name_space:NameFinder, extra_characters:list[Actor], controllers:CharacterControlFactory, *, every_turn_requirement:list[Restriction]=None):
        self.game_details    = details
        self.name_space      = name_space
        self.character_order:list[Actor] = self.name_space.get_from_name(category='actor')
        self.controllers     = controllers
        self.every_turn_requirement = every_turn_requirement
        self.translator      = get_input_translator()
        self.current_turn    = 0
        self.moves           = 0
        self.action_dict     = dict[Action,GameAction]({
            self.name_space.get_from_name('look',      'action')[0]: LookAction(self.name_space.get_from_name('look',     'action')[0]),
            self.name_space.get_from_name('walk',      'action')[0]: WalkAction(self.name_space.get_from_name('walk',     'action')[0]),
            self.name_space.get_from_name('wait',      'action')[0]: WaitAction(self.name_space.get_from_name('wait',     'action')[0]),
            self.name_space.get_from_name('take',      'action')[0]: TakeAction(self.name_space.get_from_name('take',     'action')[0], "inventory", cant_take_text="You can't take",     empty_take_text="Take what?", full_pack_text="doesn't fit in your inventory.",     taken_text="Taken.", not_taken_text="No items were taken."),
            self.name_space.get_from_name('wear',      'action')[0]: TakeAction(self.name_space.get_from_name('wear',     'action')[0], "wearing",   cant_take_text="You can't wear",     empty_take_text="Wear what?", full_pack_text="doesn't fit over your many layers.", taken_text="Worn.",  not_taken_text="No items were worn."),
            self.name_space.get_from_name('drop',      'action')[0]: DropAction(self.name_space.get_from_name('drop',     'action')[0], "inventory", cant_drop_text="You can't drop",     empty_drop_text="Drop what?",     dropped_text="Dropped.", no_drop_text="No items were dropped."),
            self.name_space.get_from_name('take off',  'action')[0]: DropAction(self.name_space.get_from_name('take off', 'action')[0], "wearing",   cant_drop_text="You can't take off", empty_drop_text="Take off what?", dropped_text="Dropped.", no_drop_text="No items were taken off."),
            self.name_space.get_from_name('inventory', 'action')[0]: CheckInventoryAction(self.name_space.get_from_name('inventory', 'action')[0], "inventory", contains_text="Your inventory contains", empty_text="Your inventory is empty."),
            self.name_space.get_from_name('wearing',   'action')[0]: CheckInventoryAction(self.name_space.get_from_name('wearing',   'action')[0], "wearing",   contains_text="You are wearing", empty_text="You have nothing on but the clothes you woke up in."),
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
            feedback = Feedback(plain_text_description(inputs.message), Response(character, action, False), turns=0)
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
