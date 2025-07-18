from utils.relator import NameFinder
from models.actors import Target
from readin.description_helpers import plain_text
from readin.utils import sdg_from_parts

def add_to_name_space(name_space:NameFinder) -> None:
    sdg = sdg_from_parts(
        unbreakable_states=[name_space.get_from_id("visible",  "state")],
        state_graphs      =[name_space.get_from_id("takeable", "stategraph")],
        name_space        =name_space
    )

    puzzle = Target(
        name="puzzle",
        aliases=["jigsaw puzzle"],
        description=(plain_text, "an imcomplete jigsaw puzzle"),
        states=sdg,
        weight=5,
        value=3,
        size=1,
    )

    name_space.add(puzzle)
