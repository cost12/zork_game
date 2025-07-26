from utils.relator import NameFinder
from models.actors import Target
from models.response import StaticResponse
from readin.description_helpers import Description, PlainTextDescription, PlainTextContext
from readin.utils import sdg_from_parts

def add_to_name_space(name_space:NameFinder) -> None:
    sdg = sdg_from_parts(
        unbreakable_states=[name_space.get_from_id("visible",   "state")],
        state_graphs      =[name_space.get_from_id("takeable",  "stategraph")],
        breakable_states  =[name_space.get_from_id("flippable", "stategraph")],
        name_space        =name_space
    )

    hourglass = Target(
        name="hourglass",
        aliases=["herbs"],
        description=Description[PlainTextContext](PlainTextContext("an ancient fragile hourglass"), PlainTextDescription()),
        states=sdg,
        weight=0.5,
        value=5,
        size=1,
        target_responses={
            name_space.get_from_id("toggle", "action") : StaticResponse("Grains of sand tumble through the hourglass, mezmerising you.")
        },
        state_responses={
            name_space.get_from_id("broken",  "state") : StaticResponse("The hourglass easily snaps, the sang spilling. You hear a whooshing sound, as if some spell or curse has been lifted somewhere."),
            name_space.get_from_id("held",    "state") : StaticResponse("The hourglass is delicate in your grasp.")
        }
    )

    name_space.add(hourglass)
