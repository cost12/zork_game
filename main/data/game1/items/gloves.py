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

    gloves = Target(
        name="thick gloves",
        aliases=["gloves"],
        description_context=PlainTextContext("a pair of thick-hide gloves"),
        description_strategy=PlainTextDescription(),
        weight=2,
        value=3,
        size=1,
        target_info=TargetInfo(
            states=sdg,
            target_responses={
                name_space.get_from_id("break",   "action") : plain_text_description("You tear at the jacket, but it must have been made by valiant manufacturers- you can't seem to do any damage.")
            },
            state_responses={
                name_space.get_from_id("held",     "state") : plain_text_description("The gloves feel tough yet warm."),
                name_space.get_from_id("worn",     "state") : plain_text_description("You put the gloves on, feeling their warm protection"),
                name_space.get_from_id("wearable", "state") : plain_text_description("You take the gloves off."),
                name_space.get_from_id("broken",   "state") : plain_text_description("You tear at the gloves, hampering their ability to keep your little fingies warm. uWu!")
            }
        )
    )

    name_space.add(gloves)
