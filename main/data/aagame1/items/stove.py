from utils.relator import NameFinder
from models.actors import Target
from models.response import StaticResponse
from readin.description_helpers import Description, PlainTextDescription, PlainTextContext
from readin.utils import sdg_from_parts

def add_to_name_space(name_space:NameFinder) -> None:
    sdg = sdg_from_parts(
        unbreakable_states=[name_space.get_from_id("visible", "state")],
        state_graphs      =[name_space.get_from_id("switch",  "stategraph")],
        name_space        =name_space
    )

    stove = Target(
        name="stove",
        description=Description[PlainTextContext](PlainTextContext("a battered, greasy stove"), PlainTextDescription()),
        states=sdg,
        weight=5,
        value=3,
        size=1,
        target_responses={
            name_space.get_from_id("take", "action")  : StaticResponse("And do what with it? Nice try.")
        },
        state_responses={
            name_space.get_from_id("on",     "state") : StaticResponse("The stove clicks, but nothing happens."),
            name_space.get_from_id("off",    "state") : StaticResponse("The stove is off."),
            name_space.get_from_id("broken", "state") : StaticResponse("You dent the stove.")
        }
    )

    name_space.add(stove)
