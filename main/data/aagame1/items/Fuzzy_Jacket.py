from utils.relator import NameFinder
from models.actors import Target
from models.response import StaticResponse
from readin.description_helpers import Description, PlainTextDescription, PlainTextContext
from readin.utils import sdg_from_parts

def add_to_name_space(name_space:NameFinder) -> None:
    sdg = sdg_from_parts(
        unbreakable_states=[name_space.get_from_id("visible",   "state")],
        state_graphs      =[name_space.get_from_id("flammable", "stategraph"),
                            name_space.get_from_id("wearable",  "stategraph")],
        name_space        =name_space
    )

    jacket = Target(
        name="fuzzy jacket",
        aliases=["jacket"],
        description=Description[PlainTextContext](PlainTextContext("a poofy and comfortable winter jacket, just your size"), PlainTextDescription()),
        states=sdg,
        weight=3,
        value=5,
        size=1,
        target_responses={
            name_space.get_from_id("break",   "action") : StaticResponse("You tear at the jacket, but it must have been made by valiant manufacturers- you can't seem to do any damage.")
        },
        state_responses={
            name_space.get_from_id("held",     "state") : StaticResponse("You take the puffy jacket."),
            name_space.get_from_id("worn",     "state") : StaticResponse("The jacket smells a little musky as you don it, but it should keep you very warm."),
            name_space.get_from_id("wearable", "state") : StaticResponse("You take the jacket off, revealing your bare, hairy chest."),
        }
    )

    name_space.add(jacket)
