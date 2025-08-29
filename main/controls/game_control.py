from typing import Any

from models.actors              import Actor, Location, World
from models.named               import Action
from factories.factories        import CharacterControlFactory
from controls.character_control import CommandLineController, Feedback, CharacterController
from controls.translate         import get_input_translator
from utils.relator              import NameFinder
from utils.constants            import DEBUG_INPUT
from readin.restriction_helpers import Restriction
from readin.description_helpers import plain_text_description, DescriptionContext

class GameState:
    """Represents an instance of a Zork game
    """

    def __init__(self, details:dict[str,Any], world:World, name_space:NameFinder, extra_characters:list[Actor], controllers:CharacterControlFactory, *, every_turn_requirement:list[Restriction]=None):
        self.game_details    = details
        self.world           = world
        self.name_space      = name_space
        self.character_order:list[Actor] = self.name_space.get_from_name(category='actor')
        self.controllers     = controllers
        self.every_turn_requirement = every_turn_requirement
        self.translator      = get_input_translator()
        self.current_turn    = 0
        self.moves           = 0
        i = 0
        start_rooms = [room for room in self.name_space.get_from_name(category='location') if isinstance(room, Location) and room.is_start_location()]
        for character in extra_characters:
            start_room = start_rooms[i%len(start_rooms)]
            controllers.create_character(character, CommandLineController())
            world.item_locations.add_character(character, start_room)
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
            feedback = Feedback(
                plain_text_description(inputs.message),
                DescriptionContext(self.world.item_locations, action, False, character, None, None),
                turns=0,
                moves=1,
                score=0
            )
        valid, inputs, response = action.check_inputs(inputs)
        if valid:
            feedback = action.take_action(character, inputs)
        else:
            feedback = Feedback(
                response,
                DescriptionContext(self.world.item_locations, action, False, character, None, None),
                turns=0,
                moves=1,
                score=0
            )
        self.current_turn += feedback.turns
        self.moves += feedback.moves
        return feedback
