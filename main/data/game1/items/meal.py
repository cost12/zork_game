from utils.relator import NameFinder
from models.actors import Target, TargetInfo
from readin.description_helpers import PlainTextDescription, PlainTextContext, plain_text_description
from readin.utils import sdg_from_parts

def add_to_name_space(name_space:NameFinder) -> None:
    sdg = sdg_from_parts(
        unbreakable_states=[name_space.get_from_id("visible",   "state"),
                            name_space.get_from_id("edible",    "state")],
        state_graphs      =[name_space.get_from_id("breakable", "stategraph")],
        name_space        =name_space
    )

    meal = Target(
        name="meal",
        description_context=PlainTextContext("a decadent, steaming meal"),
        description_strategy=PlainTextDescription(),
        weight=3,
        value=3,
        size=2,
        target_info=TargetInfo(
            states=sdg,
            target_responses={
                name_space.get_from_id("eat",   "action") : plain_text_description("Yum! That was quite filling!")
            },
            state_responses={
                name_space.get_from_id("held",   "state") : plain_text_description("It's a bit messy to be taking with you..."),
                name_space.get_from_id("broken", "state") : plain_text_description("Now that's just gratuitous!")
            }
        )
    )

    name_space.add(meal)
