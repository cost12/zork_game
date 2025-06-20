from models.named  import Action
from models.actors import Actor, Target, LocationDetail
from utils.utils   import list_to_str

def plain_text(action:Action, success:bool, character:Actor, target:Target, tool:Target, text:str) -> str:
    return text

def contents_text(action:Action, success:bool, character:Actor, target:Target, tool:Target, info:tuple[LocationDetail,str,str]) -> str:
    location_detail, empty_text, full_text = info
    contents = location_detail.list_contents_visible_to(character)
    if len(contents) == 0:
        return empty_text
    return f"{full_text} {list_to_str([item.get_description_to(character) for item in contents])}"