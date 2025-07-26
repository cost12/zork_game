from utils.relator import NameFinder
from models.actors import Target
from models.response import StaticResponse
from readin.description_helpers import Description, PlainTextDescription, PlainTextContext
from readin.utils import sdg_from_parts

def add_to_name_space(name_space:NameFinder) -> None:
    sdg = sdg_from_parts(
        unbreakable_states=[name_space.get_from_id("visible",   "state")],
        state_graphs      =[name_space.get_from_id("takeable",  "stategraph")],
        name_space        =name_space
    )

    skateboard = Target(
        name="skateboard",
        description=Description[PlainTextContext](PlainTextContext("a classic skateboard with Rob Dyrdek's brand designs on the bottom"), PlainTextDescription()),
        states=sdg,
        weight=4,
        value=1,
        size=5,
        state_responses={
            name_space.get_from_id("held", "state") : StaticResponse("You take the skateboard and immediately look 20% cooler")
        }
    )

    name_space.add(skateboard)
