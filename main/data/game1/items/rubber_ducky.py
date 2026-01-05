from utils.relator import NameFinder
from models.actors import Target, TargetInfo
from readin.description_helpers import PlainTextDescription, PlainTextContext, plain_text_description
from readin.utils import sdg_from_parts

def add_to_name_space(name_space:NameFinder) -> None:
    sdg = sdg_from_parts(
        unbreakable_states=[name_space.get_from_id("visible",   "state")],
        state_graphs      =[name_space.get_from_id("takeable",  "stategraph")],
        name_space        =name_space
    )

    duck = Target(
        name="rubber ducky",
        aliases=["rubber duck", "duck", "ducky"],
        description_context=PlainTextContext("a classic yellow rubber ducky"),
        description_strategy=PlainTextDescription(),
        weight=1,
        value=1,
        size=1,
        target_info=TargetInfo(
            states=sdg,
            target_responses={
                name_space.get_from_id("squeeze", "action") : plain_text_description("SQUEAK"),
                name_space.get_from_id("break",   "action") : plain_text_description("It's rubber, how do you want to break it?")
            },
            state_responses={
                name_space.get_from_id("held",     "state") : plain_text_description("You take the rubber ducky. It squeaks when you squeeze it.")
            }
        )
    )

    name_space.add(duck)
