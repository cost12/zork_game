from utils.relator              import NameFinder
from models.actors              import Target, TargetInfo
from readin.description_helpers import PlainTextContext, PlainTextDescription, plain_text_description
from readin.utils               import sdg_from_parts

def add_to_name_space(name_space:NameFinder) -> None:
    sdg = sdg_from_parts(
        unbreakable_states=[name_space.get_from_id("visible",  "state")],
        state_graphs      =[name_space.get_from_id("takeable sg", "stategraph")],
        breakable_states  =[name_space.get_from_id("bouncy",   "state"),
                            name_space.get_from_id("throwable", "state")],
        name_space        =name_space
    )

    basketball = Target(
        name="Basketball",
        description_context=PlainTextContext("a well-worn basketball"),
        description_strategy=PlainTextDescription(),
        weight=2,
        value=3,
        size=3,
        target_info=TargetInfo(
            states=sdg,
            target_responses={name_space.get_from_id("takeable", "state") : plain_text_description("You can feel many hours of play on the ball's surface")},
            state_responses ={name_space.get_from_id("broken",   "state") : plain_text_description("The basketball deflates sadly, making itself unusable")}
        ),
    )

    name_space.add(basketball)
