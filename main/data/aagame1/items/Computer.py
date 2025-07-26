from utils.relator import NameFinder
from models.actors import Target
from models.response import StaticResponse
from readin.description_helpers import plain_text
from readin.utils import sdg_from_parts

def add_to_name_space(name_space:NameFinder) -> None:
    sdg = sdg_from_parts(
        unbreakable_states=[name_space.get_from_id("visible",   "state")],
        state_graphs      =[name_space.get_from_id("switch",    "stategraph")],
        breakable_states  =[name_space.get_from_id("typeable",  "state"),
                            name_space.get_from_id("readable",  "state")],
        name_space        =name_space
    )

    computer = Target(
        name="computer",
        description=Description[PlainTextContext](PlainTextContext("an old-school computer hums soflty, the gentle light of its screen illuminating the space"), PlainTextDescription()),
        states=sdg,
        weight=100,
        value=100,
        size=25,
        target_responses={
            name_space.get_from_id("take", "action")  : StaticResponse("The computer is a bit heavy for you. Plus, you don't want to risk unplugging it!")
        },
        state_responses={
            name_space.get_from_id("on",     "state") : StaticResponse("The computer is on."),
            name_space.get_from_id("off",    "state") : StaticResponse("The computer is off."),
            name_space.get_from_id("broken", "state") : StaticResponse("The screen breaks as you destroy a perfectly fine old machine.")
        }
    )

    name_space.add(computer)
