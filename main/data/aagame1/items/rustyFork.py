from utils.relator import NameFinder
from models.actors import Target
from models.response import StaticResponse
from readin.description_helpers import plain_text
from readin.utils import sdg_from_parts

def add_to_name_space(name_space:NameFinder) -> None:
    sdg = sdg_from_parts(
        unbreakable_states=[name_space.get_from_id("visible",   "state")],
        state_graphs      =[name_space.get_from_id("takeable",  "stategraph")],
        name_space        =name_space
    )

    fork = Target(
        name="rusty fork",
        aliases=["fork"],
        description=(plain_text, "an old rusty metal fork"),
        states=sdg,
        weight=1,
        value=1,
        size=1,
        target_responses={
            name_space.get_from_id("squeeze", "action") : StaticResponse("SQUEAK"),
            name_space.get_from_id("break",   "action") : StaticResponse("You lack the brute strength necessary to break a fork.")
        },
        state_responses={
            name_space.get_from_id("held",     "state") : StaticResponse("You take the fork. Watch out for tetanus!")
        }
    )

    name_space.add(fork)
