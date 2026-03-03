from utils.relator              import NameFinder
from models.actors              import Target, TargetInfo
from readin.description_helpers import PlainTextDescription, PlainTextContext, plain_text_description
from readin.utils               import sdg_from_parts

def add_to_name_space(name_space:NameFinder) -> None:
    sdg = sdg_from_parts(
        unbreakable_states=[name_space.get_from_id("visible",    "state")],
        state_graphs      =[name_space.get_from_id("open_close sg", "stategraph")],
        name_space        =name_space
    )

    door = Target(
        name="trunk door",
        aliases=["door"],
        description_context=PlainTextContext("a trunk door"),
        description_strategy=PlainTextDescription(),
        weight=3,
        value=3,
        size=5,
        target_info=TargetInfo(
            states=sdg,
            target_responses={
                name_space.get_from_id("take",  "action") : plain_text_description("???"),
                name_space.get_from_id("break", "action") : plain_text_description("You can't seem to break it.")
            }
        )
    )

    name_space.add(door)
