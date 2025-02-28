from enum import Enum

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

class Room:
    """Base class for rooms that a Character can move between
    """
    def __init__(self, name:str, description:str):
        """Create a Room

        :param name: The name of the Room
        :type name: str
        :param description: A description of the room
        :type description: str
        """
        self.name = name
        self.description = description

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

class Layout:
    """A layout of rooms that a Character can move between
    """

    def __init__(self):
        """Creates a Layout
        """
        self.layout = dict[Room, dict[Direction,Room]]()
        