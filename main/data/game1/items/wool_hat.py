from utils.relator import NameFinder
from models.actors import Target, TargetInfo
from readin.description_helpers import PlainTextDescription, PlainTextContext, plain_text_description
from readin.utils import sdg_from_parts

def add_to_name_space(name_space:NameFinder) -> None:
    sdg = sdg_from_parts(
        unbreakable_states=[name_space.get_from_id("visible",   "state")],
        state_graphs      =[name_space.get_from_id("wearable sg", "stategraph")],
        name_space        =name_space
    )

    hat = Target(
        name="wool hat",
        aliases=["hat", "knit hat", "cap", "grandma's hat", "granny cap"],
        description_context=PlainTextContext("a lovely knit hat, as if done by a grandmother"),
        description_strategy=PlainTextDescription(),
        weight=1,
        value=3,
        size=1,
        target_info=TargetInfo(
            states=sdg,
            state_responses={
                name_space.get_from_id("held",     "state") : plain_text_description("You take the woolen hat, feeling its soft warmth."),
                name_space.get_from_id("worn",     "state") : plain_text_description("Though it itches minorly, the hat should keep your head nice and cozy."),
                name_space.get_from_id("wearable", "state") : plain_text_description("You take the hat off."),
                name_space.get_from_id("broken",   "state") : plain_text_description("You rip the hat to shreds, defiling the gentle work of a caring, lovely grandma somewhere.")
            }
        )
    )

    name_space.add(hat)
