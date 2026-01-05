from utils.relator import NameFinder
from models.actors import Target, TargetInfo
from readin.description_helpers import PlainTextDescription, PlainTextContext, plain_text_description
from readin.utils import sdg_from_parts

def add_to_name_space(name_space:NameFinder) -> None:
    sdg = sdg_from_parts(
        unbreakable_states=[name_space.get_from_id("visible",  "state")],
        state_graphs      =[name_space.get_from_id("takeable", "stategraph")],
        breakable_states  =[name_space.get_from_id("sharp",    "state")],
        name_space        =name_space
    )

    sword = Target(
        name="sword",
        description_context=PlainTextContext("a classic yet deadly-looking sword, glinting, as if mocking its slain enemies"),
        description_strategy=PlainTextDescription(),
        weight=3,
        value=3,
        size=5,
        target_info=TargetInfo(
            states=sdg,
            target_responses={
                name_space.get_from_id("break", "action") : plain_text_description("A blade of this making cannot be broken by one such as you. HA!")
            },
            state_responses={
                name_space.get_from_id("held",   "state") : plain_text_description("The sword is well-balanced. Its maker speaks to you through it, warning you of the deathly power it holds, expressing himself through sheer emotion, lest words sully the message's import."),
            }
        )
    )

    name_space.add(sword)
