from utils.relator import NameFinder
from models.actors import Target
from models.response import StaticResponse
from readin.description_helpers import plain_text
from readin.utils import sdg_from_parts

def add_to_name_space(name_space:NameFinder) -> None:
    sdg = sdg_from_parts(
        unbreakable_states=[name_space.get_from_id("visible",   "state")],
        state_graphs      =[name_space.get_from_id("takeable",  "stategraph"),
                            name_space.get_from_id("flammable", "stategraph")],
        breakable_states  =[name_space.get_from_id("readable",  "state")],
        name_space        =name_space
    )

    keys = Target(
        name="keys",
        description=(plain_text, "a simple keychain with a single car key, an archaic brass key, and a tiny plushie of Nami from One Piece"),
        states=sdg,
        weight=1,
        value=1,
        size=1,
        target_responses={
            name_space.get_from_id("take off", "action") : StaticResponse("You try to remove it from the keychain's ring but your fingernails are too short to separate the ring's loops."),
            name_space.get_from_id("admire",   "action") : StaticResponse("Nami so pretty.")
        },
        state_responses={
            name_space.get_from_id("taken",  "state") : StaticResponse("You take the jangling keychain."),
            name_space.get_from_id("broken", "state") : StaticResponse("You rip the book in two, destroying its readability. Nice going...")
        }
    )

    name_space.add(keys)
