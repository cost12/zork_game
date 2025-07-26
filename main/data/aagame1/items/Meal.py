from utils.relator import NameFinder
from models.actors import Target
from models.response import StaticResponse
from readin.description_helpers import plain_text
from readin.utils import sdg_from_parts

def add_to_name_space(name_space:NameFinder) -> None:
    sdg = sdg_from_parts(
        unbreakable_states=[name_space.get_from_id("visible",   "state"),
                            name_space.get_from_id("edible",    "state")],
        state_graphs      =[name_space.get_from_id("breakable", "stategraph")],
        name_space        =name_space
    )

    meal = Target(
        name="meal",
        description=Description[PlainTextContext](PlainTextContext("a decadent, steaming meal"), PlainTextDescription()),
        states=sdg,
        weight=3,
        value=3,
        size=2,
        target_responses={
            name_space.get_from_id("eat",   "action") : StaticResponse("Yum! That was quite filling!")
        },
        state_responses={
            name_space.get_from_id("held",   "state") : StaticResponse("It's a bit messy to be taking with you..."),
            name_space.get_from_id("broken", "state") : StaticResponse("Now that's just gratuitous!")
        }
    )

    name_space.add(meal)
