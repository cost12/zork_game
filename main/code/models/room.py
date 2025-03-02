from enum import Enum
from typing import Optional

from code.models.item import Item
from code.models.character import Character
from code.models.action import Action

class Direction(Enum):
    """The Directions a Character can move to get from Room to Room
    """
    NORTH     = 0
    NORTHEAST = 1
    EAST      = 2
    SOUTHEAST = 3
    SOUTH     = 4
    SOUTHWEST = 5
    WEST      = 6
    NORTHWEST = 7
    UP        = 8
    DOWN      = 9

class Exit:
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
        pass

class Room:
    """Base class for rooms that a Character can move between
    """
    def __init__(self, name:str, description:str, exits:dict[Direction,Exit], items:Optional[list[Item]]=None, characters:Optional[list[Character]]=None, actions:Optional[list[Action]]=None):
        """Creates a Room

        :param name: The name of the Room
        :type name: str
        :param description: A description of the room
        :type description: str
        :param exits: A dict from the directions to the Exits
        :type exits: dict[Direction, Exit]
        :param items: Any Items initially in the room, defaults to None
        :type items: list[Item], optional
        :param characters: Any Characters initially in the room, defaults to None
        :type characters: list[Character], optional
        :param actions: Any additional Actions that can be performed in this room, defaults to None
        :type actions: list[Action], optional
        """
        self.name = name
        self.description = description
        self.exits = exits
        self.items = list[Item]() if items is None else items
        self.characters = list[Character] if characters is None else characters
        self.actions = list[Action]() if actions is None else actions

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
    
    def get_exits(self) -> dict[Direction, Exit]:
        """Get the Exits from the Room

        :return: The exits from the Room
        :rtype: dict[Direction, Exit]
        """
        return self.exits
    
