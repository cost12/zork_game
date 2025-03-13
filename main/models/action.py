from typing import Optional

class Named:

    def __init__(self, name:str, aliases:Optional[list[str]]=None):
        self.name = name
        self.aliases = [name.lower()] if aliases is None else [alias.lower() for alias in aliases]

    def __repr__(self):
        return f"[Named: {self.name}]"

    def __eq__(self, other):
        return isinstance(other, Named) and other.name.lower() == self.name.lower()
    
    def __hash__(self):
        return hash(self.name.lower())

    def get_name(self) -> str:
        return self.name

    def get_aliases(self) -> list[str]:
        return self.aliases

class Action(Named):
    """Base class for an Action that a Character can make
    """

    def __init__(self, name:str, aliases:Optional[list[str]]=None):
        super().__init__(name, aliases)

    def __repr__(self):
        return f"[Action: {self.name}]"
    
    def act(self):
        pass
