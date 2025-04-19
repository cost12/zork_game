from dataclasses import dataclass

from models.response import ResponseString, Response
import views.string_views as views

#@dataclass(frozen=True)
class Feedback:
    """This is a dataclass.
    Represents a response from the GameState to the CharacterController after an Action
    """
    def __init__(self, response_string:ResponseString, response:Response, moves:int=1, turns:int=1, score:int=0):
        self.response_string = response_string
        self.response = response
        self.moves = moves
        self.turns = turns
        self.score = score

    def get_success(self) -> bool:
        return self.response.success

    def as_string(self) -> str:
        """A string representation of the Feedback to be output to the command line.

        :return: A string representation of the Feedback
        :rtype: str
        """
        return self.response_string.as_string(self.response)

class CharacterController:
    """This is an abstract class and should not be initialized.
    Determines which Action a Character should complete on their turn.
    Receives Feedback from completing Actions or from noticing other Characters
    This Feedback can be used to determine future Actions.
    """

    def make_move(self) -> str:
        """Returns a string representation of the Action to be attempted.
        No information is passed in, but information can be stored from Feedback to help make a decision.

        :return: A string representing the Action to be attempted.
        :rtype: str
        """
        pass

    def feedback(self, feedback:Feedback) -> None:
        """Gives the CharacterController information about recently attempted Actions.
        Future decisions can use this Feedback to determine which Action to perform.

        :param feedback: Feedback from a recently attempted Action. Typically by the controlled Character, but could be from another Character that the controlled Character perceives in some way (sees, hears, smells, ...)
        :type feedback: Feedback
        """
        pass

class NPCController(CharacterController):
    """Inherits from CharacterController.
    Controls an NPC Character and takes the wait Action every turn.
    """
    def __init__(self) -> 'NPCController':
        """Creates an NPCController
        """
        pass

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
        pass

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
    
    def feedback(self, feedback:Feedback) -> None:
        """Reads the moves, turns, and score from the Feedback and prints the rest out to command line for the user to read.

        :param feedback: Feedback from a recently attempted Action. Typically by the controlled Character, but could be from another Character that the controlled Character perceives in some way (sees, hears, smells, ...)
        :type feedback: Feedback
        """
        self.moves += feedback.moves
        self.turns += feedback.turns
        self.score += feedback.score
        print(feedback.as_string())
