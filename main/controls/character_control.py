from abc import ABC, abstractmethod
from dataclasses import dataclass

import views.string_views as views
from models.named import Named
from readin.description_helpers import Description, DescriptionContext

@dataclass(frozen=True)
class Feedback:
    description : Description
    context     : DescriptionContext
    score       : int
    moves       : int = 1
    turns       : int = 1

    def get_success(self) -> bool:
        return self.context.success

    def as_string(self) -> str:
        return self.description.describe(self.context)

class CharacterController(ABC):
    """This is an abstract class and should not be initialized.
    Determines which Action a Character should complete on their turn.
    Receives Feedback from completing Actions or from noticing other Characters
    This Feedback can be used to determine future Actions.
    """

    @abstractmethod
    def make_move(self) -> str:
        """Returns a string representation of the Action to be attempted.
        No information is passed in, but information can be stored from Feedback to help make a decision.

        :return: A string representing the Action to be attempted.
        :rtype: str
        """

    @abstractmethod
    def feedback(self, feedback:Feedback) -> None:
        """Gives the CharacterController information about recently attempted Actions.
        Future decisions can use this Feedback to determine which Action to perform.

        :param feedback: Feedback from a recently attempted Action. Typically by the controlled Character, but could be from another Character that the controlled Character perceives in some way (sees, hears, smells, ...)
        :type feedback: Feedback
        """

    @abstractmethod
    def decide(self, options:list[tuple[list[Named],list[str]]]) -> int:
        """If the character makes an ambiguous move, this helps disambiguate it

        :param options: The possible interpretations. Each tuple matches the ambiguous text to a possible interpretation
        :type options: list[tuple[list[Named],list[str]]]
        :return: The index of the correct interpretation
        :rtype: int
        """

class NPCController(CharacterController):
    """Inherits from CharacterController.
    Controls an NPC Character and takes the wait Action every turn.
    """
    def __init__(self) -> 'NPCController':
        """Creates an NPCController
        """

    def make_move(self) -> str:
        """Controls which Action the NPC Character will attempt to make. Always chooses wait.

        :return: 'wait'
        :rtype: str
        """
        return 'wait'

    def feedback(self, feedback:Feedback) -> None:
        """Ignores the feedback.

        :param feedback: Feedback from a recently attempted Action. Typically by the controlled Character, but could be from another Character that the controlled Character perceives in some way (sees, hears, smells, ...)
        :type feedback: Feedback
        """

    def decide(self, options):
        return 0

class CommandLineController(CharacterController):
    """Inherits from CharacterController.
    Controller for a user controlled Character. Stores moves, turns, and score. 
    Any other details are printed to command line for the user to remember.
    Actions are read in from the command line.
    """

    def __init__(self):
        """Creates a CommandLineController
        """
        self.moves = 0
        self.turns = 0
        self.score = 0

    def make_move(self) -> str:
        """Prompts the user to enter their move into the command line and returns the user response

        :return: The user's command line input
        :rtype: str
        """
        return input(views.input_prompt(self.moves,self.turns,self.score))

    def decide(self, options:list[tuple[list[Named],list[str]]]) -> int:
        """If the character makes an ambiguous move, this helps disambiguate it

        :param options: The possible interpretations. Each tuple matches the ambiguous text to a possible interpretation
        :type options: list[tuple[list[Named],list[str]]]
        :return: The index of the correct interpretation
        :rtype: int
        """
        texts = []
        for _,words in options:
            text = " ".join(words)
            if text not in texts:
                texts.append(text)
        print(f"By \"{'"/"'.join(texts)}\" did you mean:")
        i = 0
        for objects,_ in options:
            print(f"[{i}] {" ".join([f"{obj.get_name()} ({obj.get_id()})" for obj in objects])}")
            i += 1
        response = input("> ")
        print("")
        try:
            index = int(response)
            if 0 <= index and index < len(options):
                return index
        except ValueError:
            i=0
            for objects,_ in options:
                for obj in objects:
                    if response.lower() == obj.get_id():
                        return i
                i += 1
        print("Invalid response, please either give the index or id.")
        return self.decide(options)

    def feedback(self, feedback:Feedback) -> None:
        """Reads the moves, turns, and score from the Feedback and prints the rest out to command line for the user to read.

        :param feedback: Feedback from a recently attempted Action. Typically by the controlled Character, but could be from another Character that the controlled Character perceives in some way (sees, hears, smells, ...)
        :type feedback: Feedback
        """
        self.moves += feedback.moves
        self.turns += feedback.turns
        self.score += feedback.score
        print(feedback.as_string())
