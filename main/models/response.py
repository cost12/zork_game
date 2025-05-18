from typing import Optional, TYPE_CHECKING
import random

if TYPE_CHECKING:
    from models.actors import Actor, Target
    from models.named  import Action
    from models.state  import State
from utils.constants   import *

class Response:
    """Represents a Character, Item, or environment response to a Character's Action.
    It contains a representation in Object form to allow it to be interpreted
    easily by (simple) AI agents when passed into functions.
    """
    def __init__(self, character:'Actor', action:'Action', success:bool, *, target:'Target'=None, tool:'Target'=None):
        self.character = character
        self.action    = action
        self.success   = success
        self.target    = target
        self.tool      = tool

class ResponseString:
    """Represents a Character, Item, or environment response to a Character's Action.
    It contains a representation in string form to allow it to be interpreted
    easily by humans players in the command line.
    """
    def __init__(self):
        pass

    def as_string(self, response:Response) -> Optional[str]:
        pass

class CombinationResponse(ResponseString):
    """A response that combines mutiple response types into 1 string.
    """
    def __init__(self, responses:list[ResponseString], *, joiner:str=""):
        if DEBUG_RESPONSES:
            for response in responses:
                if isinstance(response, str):
                    raise RuntimeError()
        self.responses = responses
        self.joiner = joiner

    def as_string(self, response:Response) -> Optional[str]:
        if DEBUG_RESPONSES:
            for r in self.responses:
                if r is None:
                    for r2 in self.responses:
                        if r2 is not None:
                            print(r2.as_string(response))
                        else:
                            print(None)
                    break
                if isinstance(r.as_string(response), dict):
                    print(type(r))
                    print(r.response)
        strings = [r.as_string(response) for r in self.responses if r.as_string(response) is not None]
        if len(strings) > 0:
            return f"{self.joiner}".join(strings)
        return None

class StaticResponse(ResponseString):
    """A response that does not depend on anything, it's the same thing every time.
    """
    def __init__(self, response:str):
        self.response = response

    def as_string(self, response:Response) -> Optional[str]:
        return self.response
    
class RandomResponse(ResponseString):
    """A response that can say the same thing in many ways
    """
    def __init__(self, responses:list[ResponseString]):
        self.responses = responses

    def as_string(self, response:Response):
        return random.choice(self.responses).as_string(response)

class ContentsResponse(ResponseString):
    def __init__(self, full_response:ResponseString, empty_response:ResponseString, target:'Target', *, inventory=False):
        self.full_response = full_response
        self.empty_response = empty_response
        self.target = target
        self.inventory=inventory

    def __get_list_string(self, contents:list[str]) -> str:
        if len(contents) > 0:
            if len(contents) == 1:
                return f" {contents[0]}"
            elif len(contents) == 2:
                return f" {contents[0]} and {contents[1]}"
            else:
                list_start = ", ".join(contents[:-1])
                return f" {list_start}, and {contents[-1]}"
        return ""
    
    def __inventory_list(self, contents:list[str]) -> str:
        return "\n\t".join(contents)

    def as_string(self, response:Response) -> Optional[str]:
        if self.inventory:
            if TYPE_CHECKING: assert isinstance(self.target, Actor)
            contents = self.target.get_inventory_items()
        else:
            contents = self.target.list_contents_visible_to(response.character)
        contents = [item.get_description_to(response.character).as_string(response) for item in contents]
        contents = [item for item in contents if item is not None]
        if len(contents) > 0:
            return f"{self.full_response.as_string(response)}{self.__inventory_list(contents) if self.inventory else self.__get_list_string(contents)}"
        return self.empty_response.as_string(response)

class ContentsWithStateResponse(ResponseString):
    def __init__(self, target:'Target', responses:dict['State',ResponseString], *, default:ResponseString=None):
        self.target    = target
        self.responses = responses
        self.default   = default

    def as_string(self, response:Response) -> Optional[str]:
        r = ""
        for state in self.responses:
            for item in self.target.list_contents_visible_to(response.character):
                if isinstance(item, Target):
                    if state in item.get_current_state():
                        r += f"{self.responses[state].as_string(response)} "
                        break # add each response at most once
        return r[:-1] if len(r) > 0 else self.default.as_string(response)

class ItemStateResponse(ResponseString):
    """A response that depends on the current state of an Item.
    """
    def __init__(self, target:'Target', responses:dict['State',ResponseString], *, default:ResponseString=None):
        self.target    = target
        self.responses = responses
        self.default   = default

    def as_string(self, response:Response) -> Optional[str]:
        r = ""
        for state in self.target.get_current_state():
            if state in self.responses:
                r += f"{self.responses[state].as_string(response)} "
                break
        return r[:-1] if len(r) > 0 else self.default.as_string(response)

class BackupResponse(ResponseString):

    def __init__(self, responses:list[ResponseString]):
        self.responses = responses

    def as_string(self, response:Response):
        for r in self.responses:
            if r is not None:
                string = r.as_string(response)
                if string is not None:
                    return string
        return None
