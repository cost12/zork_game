from utils.relator import NameFinder
from models.actors import Target, TargetInfo
from readin.description_helpers import PlainTextDescription, PlainTextContext, plain_text_description
from readin.utils import sdg_from_parts

def add_to_name_space(name_space:NameFinder) -> None:
    sdg = sdg_from_parts(
        unbreakable_states=[name_space.get_from_id("visible",   "state")],
        state_graphs      =[name_space.get_from_id("takeable sg", "stategraph"),
                            name_space.get_from_id("flammable sg", "stategraph")],
        breakable_states  =[name_space.get_from_id("readable",  "state")],
        name_space        =name_space
    )

    keys = Target(
        name="keys",
        description_context=PlainTextContext("a simple keychain with a single car key, an archaic brass key, and a tiny plushie of Nami from One Piece"),
        description_strategy=PlainTextDescription(),
        weight=1,
        value=1,
        size=1,
        target_info=TargetInfo(
            states=sdg,
            target_responses={
                name_space.get_from_id("take off", "action") : plain_text_description("You try to remove it from the keychain's ring but your fingernails are too short to separate the ring's loops."),
                name_space.get_from_id("admire",   "action") : plain_text_description("Nami so pretty.")
            },
            state_responses={
                name_space.get_from_id("held",      "state") : plain_text_description("You take the jangling keychain.")
            }
        )
    )

    name_space.add(keys)
