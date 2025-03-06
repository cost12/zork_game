from code.utils.alias import Alias

class Action(Alias):
    """Base class for an Action that a Character can make
    """

    def __init__(self, name:str, aliases:list[str]):
        """Creates an Action

        :param name: The name of the action
        :type name: str
        :param aliases: All string representations of the Action
        :type aliases: set[str]
        """
        self.name = name
        self.aliases = aliases

    def __repr__(self):
        return f"[Action: {self.name}]"

    def get_name(self) -> str:
        """Get the Action's name

        :return: The Action's name
        :rtype: str
        """
        return self.name
    
    def get_aliases(self) -> list[str]:
        return self.aliases
    
    def act(self):
        pass