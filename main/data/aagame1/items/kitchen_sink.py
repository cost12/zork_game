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

    sink = Target(
        name="kitchen sink",
        aliases=["sink"],
        description=Description[PlainTextContext](PlainTextContext("a stained metal sink"), PlainTextDescription()),
        states=sdg,
        weight=50, 
        value=5,
        size=30,
        target_responses={
            name_space.get_from_id("take", "action")  : StaticResponse("And do what with it? Nice try.")
        },
        state_responses={
            name_space.get_from_id("on",     "state") : StaticResponse("The sink's tap turns, buy only a sad gurgling sound emerges."),
            name_space.get_from_id("off",    "state") : StaticResponse("The sink's tap is off."),
            name_space.get_from_id("broken", "state") : StaticResponse("What are you, part of a demolition crew? The sink is dented.")
        }
    )

    name_space.add(sink)
