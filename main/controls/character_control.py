from dataclasses import dataclass

import views.string_views as views

@dataclass(frozen=True)
class Feedback:
    """This is a dataclass.
    Represents a response from the GameState to the CharacterController after an Action

    TODO: store data in a format that can be passed to either the commandline or CPU controlled character
    TODO: add Feedback about what other Characters in the room experience (or in adjacent rooms hear)
    
    :param feedback: A string summary of what the Character experiences.
    :type feedback: str
    :param success: True if the Character's attempted Action was successful. Defaults to True.
    :type success: bool
    :param moves: The number of moves taken up by the Action, typically 1. Defaults to 1.
    :type moves: int
    :param turns: The number of turns taken up by the Action, typically 0 or 1. Defaults to 1.
    :type turns: int
    :param score: The number of points gained by completing the Action, typically 0. Defaults to 0.
    :type score: int
    """
    feedback:str
    success:bool=True
    moves:int=1
    turns:int=1
    score:int=0

    def as_string(self) -> str:
        """A string representation of the Feedback to be output to the command line.

        :return: A string representation of the Feedback
        :rtype: str
        """
        return self.feedback

class CharacterController:
    """This is an abstract class and should not be initialized.
    Determines which Action a Character should complete on their turn.
    Receives Feedback from completing Actions or from noticing other Characters
    This Feedback can be used to determine future Actions.
    """

    def make_move(self) -> str:
        """Returns a string representation of the Action to be attempted.
        No information is passed in, but information can be stored from Feedback to help make a decision.

        TODO: this should probably return a tuple of an Action and inputs so CPU controlled Characters can make decisions more easily.

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

    TODO: create a more complex NPCController
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
        
        TODO: this should probably convert the string into and Action and inputs

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
