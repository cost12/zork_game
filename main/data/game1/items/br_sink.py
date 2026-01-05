from utils.relator              import NameFinder
from models.actors              import Target, TargetInfo
from readin.description_helpers import PlainTextDescription, PlainTextContext, plain_text_description
from readin.utils               import sdg_from_parts

def add_to_name_space(name_space:NameFinder) -> None:
    sdg = sdg_from_parts(
        unbreakable_states=[name_space.get_from_id("visible",   "state")],
        state_graphs      =[name_space.get_from_id("switch",  "stategraph")],
        name_space        =name_space
    )

    sink = Target(
        name="sink",
        description_context=PlainTextContext("a stained ceramic sink"),
        description_strategy=PlainTextDescription(),
        weight=50,
        value=5,
        size=30,
        target_info=TargetInfo(
            states=sdg,
            target_responses={
                name_space.get_from_id("take", "action")  : plain_text_description("And do what with it? Nice try.")
            },
            state_responses={
                name_space.get_from_id("on",     "state") : plain_text_description("The sink's tap turns, buy only a sad gurgling sound emerges."),
                name_space.get_from_id("off",    "state") : plain_text_description("The sink's tap is off."),
                name_space.get_from_id("broken", "state") : plain_text_description("What are you, part of a demolition crew? The sink shatters.")
            }
        )
    )

    name_space.add(sink)
