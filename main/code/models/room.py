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

class Exit:
    """Base class for an Exit that leads from one Room to another Room
    """
    def __init__(self, name:str, description:str, end:'Room'):
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

class Room:
    """Base class for rooms that a Character can move between
    """
    def __init__(self, name:str, description:str, exits:dict[Direction,Exit]):
        """Creates a Room

        :param name: The name of the Room
        :type name: str
        :param description: A description of the room
        :param exits: A dict from the directions to the Exits
        :type exits: dict[Direction, Exit]
        :type description: str
        """
        self.name = name
        self.description = description
        self.exits = exits

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