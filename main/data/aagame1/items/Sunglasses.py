from utils.relator import NameFinder
from models.actors import Target
from models.response import StaticResponse
from readin.description_helpers import Description, PlainTextDescription, PlainTextContext
from readin.utils import sdg_from_parts

def add_to_name_space(name_space:NameFinder) -> None:
    sdg = sdg_from_parts(
        unbreakable_states=[name_space.get_from_id("visible",   "state")],
        state_graphs      =[name_space.get_from_id("wearable",  "stategraph")],
        name_space        =name_space
    )

    glasses = Target(
        name="sunglasses",
        aliases=["glasses"],
        description=Description[PlainTextContext](PlainTextContext("a pair of simple, black plastic sunglasses"), PlainTextDescription()),
        states=sdg,
        weight=1,
        value=3,
        size=1,
        state_responses={
            name_space.get_from_id("held",     "state") : StaticResponse("You take the sunglasses."),
            name_space.get_from_id("worn",     "state") : StaticResponse("Okay cool guy. The room gets darker."),
            name_space.get_from_id("wearable", "state") : StaticResponse("You take the glasses off, getting a brighter view of your surroundings."),
            name_space.get_from_id("broken",   "state") : StaticResponse("You're able to break the sunglasses in half without much effort, but they are now unwearable.")
        }
    )

    name_space.add(glasses)
