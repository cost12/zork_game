from utils.relator import NameFinder
from models.actors import Target
from models.response import StaticResponse
from readin.description_helpers import plain_text
from readin.utils import sdg_from_parts

def add_to_name_space(name_space:NameFinder) -> None:
    sdg = sdg_from_parts(
        unbreakable_states=[name_space.get_from_id("visible",   "state")],
        state_graphs      =[name_space.get_from_id("takeable",  "stategraph"),
                            name_space.get_from_id("lightable", "stategraph"),
                            name_space.get_from_id("breakable", "stategraph")],
        name_space        =name_space
    )

    candle = Target(
        name="small candle",
        aliases=["candle"],
        description=Description[PlainTextContext](PlainTextContext("a small candle"), PlainTextDescription()),
        states=sdg,
        weight=1,
        value=1,
        size=1,
        target_responses={
            name_space.get_from_id("take", "action") : StaticResponse("You take the the candle. In your hand, the flame extinguishes with a delicate drift of fragrant smoke"),
            name_space.get_from_id("burn", "action") : StaticResponse("With what?")
        },
        state_responses={
            name_space.get_from_id("broken", "state") : StaticResponse("What is the point!")
        }
    )

    name_space.add(candle)
