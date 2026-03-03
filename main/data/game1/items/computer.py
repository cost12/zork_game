from utils.relator import NameFinder
from models.actors import Target, TargetInfo
from readin.description_helpers import PlainTextDescription, PlainTextContext, plain_text_description
from readin.utils import sdg_from_parts

def add_to_name_space(name_space:NameFinder) -> None:
    sdg = sdg_from_parts(
        unbreakable_states=[name_space.get_from_id("visible",   "state")],
        state_graphs      =[name_space.get_from_id("switch sg", "stategraph")],
        breakable_states  =[name_space.get_from_id("typeable",  "state"),
                            name_space.get_from_id("readable",  "state")],
        name_space        =name_space
    )

    computer = Target(
        name="computer",
        description_context=PlainTextContext("an old-school computer hums soflty, the gentle light of its screen illuminating the space"),
        description_strategy=PlainTextDescription(),
        weight=100,
        value=100,
        size=25,
        target_info=TargetInfo(
            states=sdg,
            target_responses={
                name_space.get_from_id("take", "action")  : plain_text_description("The computer is a bit heavy for you. Plus, you don't want to risk unplugging it!")
            },
            state_responses={
                name_space.get_from_id("on",     "state") : plain_text_description("The computer is on."),
                name_space.get_from_id("off",    "state") : plain_text_description("The computer is off."),
                name_space.get_from_id("broken", "state") : plain_text_description("The screen breaks as you destroy a perfectly fine old machine.")
            }
        )
    )

    name_space.add(computer)
