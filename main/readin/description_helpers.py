"""Commonly used functions in Target descriptions"""

from models.named  import Action
from models.state  import State
from models.actors import Actor, Target
from utils.utils   import list_to_str

def plain_text(action:Action, success:bool, character:Actor, target:Target, tool:Target, described:Target, text:str) -> str:
    return text

def contents_text(action:Action, success:bool, character:Actor, target:Target, tool:Target, described:Target, info:tuple[str,str]) -> str:
    empty_text, full_text = info
    contents = described.list_contents_visible_to(character)
    if len(contents) == 0:
        return empty_text
    return f"{full_text} {list_to_str([item.get_description_to(character) for item in contents])}"

def state_text(action:Action, success:bool, character:Actor, target:Target, tool:Target, described:Target, info:dict[State,str]) -> str:
    description = ""
    for state in described.get_current_state():
        if state in info:
            description += info[state]
    return description
