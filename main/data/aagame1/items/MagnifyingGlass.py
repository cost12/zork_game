from utils.relator import NameFinder
from models.actors import Target
from models.response import StaticResponse
from readin.description_helpers import plain_text
from readin.utils import sdg_from_parts

def add_to_name_space(name_space:NameFinder) -> None:
    sdg = sdg_from_parts(
        unbreakable_states=[name_space.get_from_id("visible",   "state")],
        state_graphs      =[name_space.get_from_id("breakable", "stategraph"),
                            name_space.get_from_id("takeable",  "stategraph")],
        name_space        =name_space
    )

    magnifying_glass = Target(
        name="magnifying glass",
        description=(plain_text, "a simple, plastic-handled magnifying glass"),
        states=sdg,
        weight=2,
        value=5,
        size=1,
        state_responses={
            name_space.get_from_id("broken", "state") : StaticResponse("Now that's just a waste!"),
            name_space.get_from_id("taken",  "state") : StaticResponse("You take the magnifying glass.")
        },
        tool_responses={
            name_space.get_from_id("burn", "action") : StaticResponse("Using the magnifying glass to refract the light, you light the candle.")
        }
    )

    name_space.add(magnifying_glass)
