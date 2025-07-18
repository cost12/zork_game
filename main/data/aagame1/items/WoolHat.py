from utils.relator import NameFinder
from models.actors import Target
from models.response import StaticResponse
from readin.description_helpers import plain_text
from readin.utils import sdg_from_parts

def add_to_name_space(name_space:NameFinder) -> None:
    sdg = sdg_from_parts(
        unbreakable_states=[name_space.get_from_id("visible",   "state")],
        state_graphs      =[name_space.get_from_id("wearable",  "stategraph")],
        name_space        =name_space
    )

    hat = Target(
        name="wool hat",
        aliases=["hat", "knit hat", "cap", "grandma's hat", "granny cap"],
        description=(plain_text, "a lovely knit hat, as if done by a grandmother"),
        states=sdg,
        weight=1,
        value=3,
        size=1,
        state_responses={
            name_space.get_from_id("taken",    "state") : StaticResponse("You take the woolen hat, feeling its soft warmth."),
            name_space.get_from_id("worn",     "state") : StaticResponse("Though it itches minorly, the hat should keep your head nice and cozy."),
            name_space.get_from_id("wearable", "state") : StaticResponse("You take the hat off."),
            name_space.get_from_id("broken",   "state") : StaticResponse("You rip the hat to shreds, defiling the gentle work of a caring, lovely grandma somewhere.")
        }
    )

    name_space.add(hat)
