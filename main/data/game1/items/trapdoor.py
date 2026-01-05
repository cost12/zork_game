from utils.relator              import NameFinder
from models.actors              import Target, TargetInfo
from readin.description_helpers import PlainTextDescription, PlainTextContext, plain_text_description
from readin.utils               import sdg_from_parts

def add_to_name_space(name_space:NameFinder) -> None:
    sdg = sdg_from_parts(
        unbreakable_states=[name_space.get_from_id("visible",   "state")],
        state_graphs      =[name_space.get_from_id("open_close", "stategraph")],
        name_space        =name_space
    )

    trapdoor = Target(
        name="trapdoor",
        aliases=["trap door", "panel"],
        description_context=PlainTextContext("a small, wooden panel, hinged along one edge"),
        description_strategy=PlainTextDescription(),
        weight=3,
        value=3,
        size=5,
        target_info=TargetInfo(
            states=sdg,
            target_responses={
                name_space.get_from_id("take",  "action") : plain_text_description("???")
            },
            state_responses={
                name_space.get_from_id("opened", "state") : plain_text_description("The trapdoor is now open."),
                name_space.get_from_id("closed", "state") : plain_text_description("The trapdoor is now closed.")
            }
        )
    )

    name_space.add(trapdoor)
