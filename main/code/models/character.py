from typing import Optional

from code.models.action import Action
from code.utils.alias import Alias

class Character(Alias):
    """Base class for all Characters, user controlled or NPCs
    """
    def __init__(self, name:str, type:str, description:str, actions:Optional[list[Action]]=None):
        """Creates a Character

        :param name: The Character's name
        :type name: str
        :param type: What type of being the character is ex: human, dragon, ...
        :type type: str
        :param description: A description of the Character
        :type description: str
        :param actions: A list of Actions that the Character has access to, defaults to None
        :type actions: list[Action], optional
        """
        self.name = name
        self.type = type
        self.description = description
        self.actions = list[Action]() if actions is None else actions

    def get_aliases(self) -> list[str]:
        return [self.name]

    def get_name(self) -> str:
        """Gets the Character's name

        :return: The Character's name
        :rtype: str
        """
        return self.name

    def get_type(self) -> str:
        """Gets the Character's type

        :return: The Character's type
        :rtype: str
        """
        return self.type

    def get_description(self) -> str:
        """Gets the Character's description

        :return: A description of the Character
        :rtype: str
        """
        return self.description

    def get_actions(self) -> str:
        """Gets the Actions available to the Character

        :return: The Actions availabe to the Character
        :rtype: str
        """
        return self.actions
