import typing

if typing.TYPE_CHECKING:
    from models.actors import Actor, Target
    from models.named  import Action

class Response:
    """Represents a Character, Item, or environment response to a Character's Action.
    It contains a representation in Object form to allow it to be interpreted
    easily by (simple) AI agents when passed into functions.
    """
    def __init__(self, character:Actor, action:Action, success:bool, *, target:Target=None, tool:Target=None):
        self.character = character
        self.action    = action
        self.target    = target
        self.tool      = tool
        self.success   = success

class ResponseString:
    """Represents a Character, Item, or environment response to a Character's Action.
    It contains a representation in string form to allow it to be interpreted
    easily by humans players in the command line.
    """
    def __init__(self):
        pass

    def as_string(self, response:Response) -> str:
        pass

class StaticResponse(ResponseString):
    """A response that does not depend on anything, it's the same thing every time.
    """
    def __init__(self, response:str):
        self.response = response

    def as_string(self, response:Response) -> str:
        return self.response

class DynamicResponse(ResponseString):
    """A response that depends on the current state of the game and the result of the Action.
    """
    def __init__(self):
        super().__init__()