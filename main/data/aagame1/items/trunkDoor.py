from utils.relator              import NameFinder
from models.actors              import Target
from models.response            import StaticResponse
from readin.description_helpers import plain_text
from readin.utils               import sdg_from_parts

def add_to_name_space(name_space:NameFinder) -> None:
    sdg = sdg_from_parts(
        unbreakable_states=[name_space.get_from_id("visible",    "state")],
        state_graphs      =[name_space.get_from_id("open_close", "stategraph")],
        name_space        =name_space
    )

    door = Target(
        name="trunk door",
        aliases=["door"],
        description=Description[PlainTextContext](PlainTextContext("a trunk door"), PlainTextDescription()),
        states=sdg,
        weight=3,
        value=3,
        size=5,
        target_responses={
            name_space.get_from_id("take",  "action") : StaticResponse("???"),
            name_space.get_from_id("break", "action") : StaticResponse("You can't seem to break it.")
        }
    )

    name_space.add(door)
