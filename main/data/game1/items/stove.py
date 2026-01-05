from utils.relator import NameFinder
from models.actors import Target, TargetInfo
from readin.description_helpers import PlainTextDescription, PlainTextContext, plain_text_description
from readin.utils import sdg_from_parts

def add_to_name_space(name_space:NameFinder) -> None:
    sdg = sdg_from_parts(
        unbreakable_states=[name_space.get_from_id("visible", "state")],
        state_graphs      =[name_space.get_from_id("switch",  "stategraph")],
        name_space        =name_space
    )

    stove = Target(
        name="stove",
        description_context=PlainTextContext("a battered, greasy stove"),
        description_strategy=PlainTextDescription(),
        weight=5,
        value=3,
        size=1,
        target_info=TargetInfo(
            states=sdg,
            target_responses={
                name_space.get_from_id("take", "action")  : plain_text_description("And do what with it? Nice try.")
            },
            state_responses={
                name_space.get_from_id("on",     "state") : plain_text_description("The stove clicks, but nothing happens."),
                name_space.get_from_id("off",    "state") : plain_text_description("The stove is off."),
                name_space.get_from_id("broken", "state") : plain_text_description("You dent the stove.")
            }
        )
    )

    name_space.add(stove)
