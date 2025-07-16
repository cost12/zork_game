from utils.relator import NameFinder
from models.actors import Target
from models.response import StaticResponse
from readin.description_helpers import plain_text
from readin.utils import sdg_from_parts

def add_to_name_space(name_space:NameFinder) -> None:
    sdg = sdg_from_parts(
        unbreakable_states=[name_space.get_from_id("visible",  "state")],
        state_graphs      =[name_space.get_from_id("takeable", "stategraph")],
        breakable_states  =[name_space.get_from_id("bouncy",   "state"), 
                            name_space.get_from_id("throwable", "state")],
        name_space        =name_space
    )

    basketball = Target(
        name="Basketball",
        description=(plain_text, "a well-worn basketball"),
        states=sdg,
        weight=2,
        value=3,
        size=3,
        target_responses={name_space.get_from_id("take", "state"): StaticResponse("You can feel many hours of play on the ball's surface")},
        state_responses={name_space.get_from_id("broken", "state"): StaticResponse("The basketball deflates sadly, making itself unusable")}
    )
    
    name_space.add(basketball)