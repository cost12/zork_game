from typing import Optional, Any

class Named:

    def __init__(self, name:str, aliases:Optional[list[str]]=None, id:str=None):
        self.name = name
        self.aliases = [name.lower()] if aliases is None else [alias.lower() for alias in aliases]
        if name.lower() not in self.aliases:
            self.aliases.append(name.lower())
        self.id = name if id is None else id # f"{name} ({str(type(self)).split(".")[-1][:-2]})" if id is None else id
        self.id = self.id.lower()

    def __repr__(self):
        return f"[Named: {self.name}]"

    def __eq__(self, other):
        return isinstance(other, Named) and other.id.lower() == self.id.lower()
    
    def __hash__(self):
        return hash(self.id.lower())

    def get_name(self) -> str:
        return self.name
    
    def get_id(self) -> str:
        return self.id

    def get_aliases(self) -> list[str]:
        return self.aliases

class Action(Named):
    """Base class for an Action that a Character can make
    """

    def __init__(self, name:str, *, aliases:Optional[list[str]]=None, is_default:bool=False, id:str=None):
        super().__init__(name, aliases, id)
        self.is_default = is_default

    def __repr__(self):
        return f"[Action: {self.name}]"
    
    def use_default(self) -> bool:
        return self.is_default

class Direction(Named):
    """The Directions a Character can move to get from Room to Room.
    """
    def __init__(self, name:str, aliases:Optional[list[str]]=None, id:str=None):
        super().__init__(name, aliases, id)

    def __repr__(self):
        return f"[Direction {self.name}]"
