from utils.relator import NameFinder
from models.actors import Target
from models.response import StaticResponse
from readin.description_helpers import plain_text
from readin.utils import sdg_from_parts

def add_to_name_space(name_space:NameFinder) -> None:
    sdg = sdg_from_parts(
        unbreakable_states=[name_space.get_from_id("visible",   "state")],
        state_graphs      =[name_space.get_from_id("switch",    "stategraph"),
                            name_space.get_from_id("takeable",  "stategraph")],
        name_space        =name_space
    )

    lantern = Target(
        name="lantern",
        aliases=["lamp"],
        description=(plain_text, "a small survival lantern"),
        states=sdg,
        weight=1,
        value=1,
        size=1,
        state_responses={
            name_space.get_from_id("on",     "state") : StaticResponse("The lantern is on."),
            name_space.get_from_id("off",    "state") : StaticResponse("The lantern is off."),
            name_space.get_from_id("broken", "state") : StaticResponse("The lantern is broken and can't be turned on. Pity..."),
            name_space.get_from_id("held",   "state") : StaticResponse("The lantern is surprisingly light!")
        }
    )

    name_space.add(lantern)
