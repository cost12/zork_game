from typing import Optional
from dataclasses import dataclass

from code.models.action import Action
from code.utils.alias import Alias

@dataclass(frozen=True)
class Direction(Alias):
    """The Directions a Character can move to get from Room to Room. 
    Immutable so it can be used in dicts.
    """
    name:int
    aliases:tuple[str]        

    @staticmethod
    def make_direction(name:str, aliases:list[str]) -> 'Direction':
        """Creates a Direction from a string and list of strings

        :param name: The name of the Direction
        :type name: str
        :param aliases: Strings that may be used to represent this direction.
        :type aliases: list[str]
        :return: A Direction created from the inputs
        :rtype: Direction
        """
        alias_set = tuple(aliases)
        return Direction(name, alias_set)

    def get_name(self) -> str:
        """Gets the name of the Direction

        :return: The name of the Direction
        :rtype: str
        """
        return self.name
    
    def get_aliases(self) -> list[str]:
        return list(self.aliases)

class Exit(Alias):
    """Base class for an Exit that leads from one Room to another Room
    """
    def __init__(self, name:str, description:str, end:'Room'):
        """Creates an Exit

        :param name: The name of the Exit
        :type name: str
        :param description: A description of the Exit
        :type description: str
        :param end: The Room that the exit leads to
        :type end: Room
        """
        self.name = name
        self.description = description
        self.end = end

    def get_aliases(self) -> list[str]:
        return [self.name]

    def get_name(self) -> str:
        """Get the Exit's name

        :return: The Exit's name
        :rtype: str
        """
        return self.name
    
    def get_description(self) -> str:
        """Get the Exit's description

        :return: The Exit's description
        :rtype: str
        """
        return self.description
    
    def get_end(self) -> 'Room':
        """Get the Room at the end of the Exit

        :return: The Room at the end of the Exit
        :rtype: Room
        """
        return self.end

    def can_exit(self) -> bool:
        """Determines whether the Character can use this exit. May have specific conditions.

        :return: True if the Character can exit, False otherwise
        :rtype: bool
        """
        return True

class Room(Alias):
    """Base class for rooms that a Character can move between
    """
    def __init__(self, name:str, description:str, actions:Optional[list[Action]]=None):
        """Creates a Room

        :param name: The name of the Room
        :type name: str
        :param description: A description of the room
        :type description: str
        :param actions: Any additional Actions that can be performed in this room, defaults to None
        :type actions: list[Action], optional
        """
        self.name = name
        self.description = description
        self.actions = list[Action]() if actions is None else actions

    def get_aliases(self) -> list[str]:
        return [self.name]

    def get_name(self) -> str:
        """Get the Room's name

        :return: The Room's name
        :rtype: str
        """
        return self.name
    
    def get_description(self) -> str:
        """Get the Room's description

        :return: The Room's description
        :rtype: str
        """
        return self.description
