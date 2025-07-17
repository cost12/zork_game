from models.state    import State
from models.actors   import Actor, Target
from models.response import ResponseString, StaticResponse

def item_state_restriction(character:Actor, info:tuple[Target,State,str]) -> tuple[bool, ResponseString]:
    item, opened, response = info
    if opened in item.get_current_state():
        return True, None
    return False, StaticResponse(response)
