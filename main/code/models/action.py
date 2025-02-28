
class Action:
    """Base class for an Action that a Character can make
    """

    def __init__(self, name:str, aliases:set[str]):
        """Creates an Action

        :param name: The name of the action
        :type name: str
        :param aliases: All string representations of the Action
        :type aliases: set[str]
        """
        self.name = name
        self.aliases = {alias.lower() for alias in aliases}

    def get_name(self) -> str:
        """Get the Action's name

        :return: The Action's name
        :rtype: str
        """
        return self.name
    
    def is_match(self, alias:str) -> bool:
        """Determine if a user input string is referncing this Action

        :param alias: The string to test
        :type alias: str
        :return: True if the string is an alias for this Action, False otherwise
        :rtype: bool
        """
        if alias.lower() in self.aliases:
            return True
        return False
    
