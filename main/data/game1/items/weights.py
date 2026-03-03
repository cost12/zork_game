from utils.relator import NameFinder
from models.actors import Target, TargetInfo
from readin.description_helpers import PlainTextDescription, PlainTextContext, plain_text_description
from readin.utils import sdg_from_parts

def add_to_name_space(name_space:NameFinder) -> None:
    sdg = sdg_from_parts(
        unbreakable_states=[name_space.get_from_id("visible",  "state"),
                            name_space.get_from_id("liftable", "state")],
        state_graphs      =[name_space.get_from_id("takeable sg", "stategraph")],
        name_space        =name_space
    )

    weights = Target(
        name="weights",
        aliases=["weight", "dumbell"],
        description_context=PlainTextContext("a lone rusty dumbell"),
        description_strategy=PlainTextDescription(),
        weight=25,
        value=10,
        size=1,
        target_info=TargetInfo(
            states=sdg,
            target_responses={
                name_space.get_from_id("lift",  "action") : plain_text_description("Nice rep. Your form isn't perfect but you feel a bit stronger for having done it."),
                name_space.get_from_id("break", "action") : plain_text_description("Ha! Even Arnold couldn't break this.")
            },
            state_responses={
                name_space.get_from_id("held",   "state") : plain_text_description("You take the weights, they are heavy.")
            }
        )
    )

    name_space.add(weights)
