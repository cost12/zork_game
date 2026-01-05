from utils.relator import NameFinder
from models.actors import Target, TargetInfo
from readin.description_helpers import PlainTextDescription, PlainTextContext, plain_text_description
from readin.utils import sdg_from_parts

def add_to_name_space(name_space:NameFinder) -> None:
    sdg = sdg_from_parts(
        unbreakable_states=[name_space.get_from_id("visible",   "state")],
        state_graphs      =[name_space.get_from_id("takeable",  "stategraph"),
                            name_space.get_from_id("lightable", "stategraph"),
                            name_space.get_from_id("breakable", "stategraph")],
        name_space        =name_space
    )

    candle = Target(
        name="square candle",
        aliases=["candle"],
        description_context=PlainTextContext("a square candle"),
        description_strategy=PlainTextDescription(),
        weight=1,
        value=1,
        size=1,
        target_info=TargetInfo(
            states=sdg,
            target_responses={
                name_space.get_from_id("take", "action") : plain_text_description("You take the the candle. In your hand, the flame extinguishes with a delicate drift of fragrant smoke"),
                name_space.get_from_id("burn", "action") : plain_text_description("With what?")
            },
            state_responses={
                name_space.get_from_id("broken", "state") : plain_text_description("What is the point!")
            }
        )
    )

    name_space.add(candle)
