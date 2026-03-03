from utils.relator import NameFinder
from models.actors import Target, TargetInfo
from readin.description_helpers import PlainTextDescription, PlainTextContext, plain_text_description
from readin.utils import sdg_from_parts

def add_to_name_space(name_space:NameFinder) -> None:
    sdg = sdg_from_parts(
        unbreakable_states=[name_space.get_from_id("visible",   "state")],
        state_graphs      =[name_space.get_from_id("breakable sg", "stategraph"),
                            name_space.get_from_id("takeable sg", "stategraph")],
        name_space        =name_space
    )

    magnifying_glass = Target(
        name="magnifying glass",
        description_context=PlainTextContext("a simple, plastic-handled magnifying glass"),
        description_strategy=PlainTextDescription(),
        weight=2,
        value=5,
        size=1,
        target_info=TargetInfo(
            states=sdg,
            state_responses={
                name_space.get_from_id("broken", "state") : plain_text_description("Now that's just a waste!"),
                name_space.get_from_id("held",   "state") : plain_text_description("You take the magnifying glass.")
            },
            tool_responses={
                name_space.get_from_id("burn",  "action") : plain_text_description("Using the magnifying glass to refract the light, you light the candle.")
            }
        )
    )

    name_space.add(magnifying_glass)
