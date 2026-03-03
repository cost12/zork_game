from utils.relator import NameFinder
from models.actors import Target, TargetInfo
from readin.description_helpers import PlainTextDescription, PlainTextContext, plain_text_description
from readin.utils import sdg_from_parts

def add_to_name_space(name_space:NameFinder) -> None:
    sdg = sdg_from_parts(
        unbreakable_states=[name_space.get_from_id("visible",   "state")],
        state_graphs      =[name_space.get_from_id("wearable sg", "stategraph")],
        name_space        =name_space
    )

    glasses = Target(
        name="sunglasses",
        aliases=["glasses"],
        description_context=PlainTextContext("a pair of simple, black plastic sunglasses"),
        description_strategy=PlainTextDescription(),
        weight=1,
        value=3,
        size=1,
        target_info=TargetInfo(
            states=sdg,
            state_responses={
                name_space.get_from_id("held",     "state") : plain_text_description("You take the sunglasses."),
                name_space.get_from_id("worn",     "state") : plain_text_description("Okay cool guy. The room gets darker."),
                name_space.get_from_id("wearable", "state") : plain_text_description("You take the glasses off, getting a brighter view of your surroundings."),
                name_space.get_from_id("broken",   "state") : plain_text_description("You're able to break the sunglasses in half without much effort, but they are now unwearable.")
            }
        )
    )

    name_space.add(glasses)
