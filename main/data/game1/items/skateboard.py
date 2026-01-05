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

    skateboard = Target(
        name="skateboard",
        description_context=PlainTextContext("a classic skateboard with Rob Dyrdek's brand designs on the bottom"),
        description_strategy=PlainTextDescription(),
        weight=4,
        value=1,
        size=5,
        target_info=TargetInfo(
            states=sdg,
            state_responses={
                name_space.get_from_id("held", "state") : plain_text_description("You take the skateboard and immediately look 20% cooler")
            }
        )
    )

    name_space.add(skateboard)
