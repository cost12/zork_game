from utils.relator import NameFinder
from models.actors import Target
from readin.description_helpers import Description, PlainTextDescription, PlainTextContext
from readin.utils import sdg_from_parts

def add_to_name_space(name_space:NameFinder) -> None:
    sdg = sdg_from_parts(
        unbreakable_states=[name_space.get_from_id("visible",   "state")],
        state_graphs      =[name_space.get_from_id("takeable",  "stategraph"),
                            name_space.get_from_id("breakable", "stategraph")],
        name_space        =name_space
    )

    wallet = Target(
        name="wallet",
        description=Description[PlainTextContext](PlainTextContext("a wallet"), PlainTextDescription()),
        states=sdg,
        weight=5,
        value=3,
        size=1,
    )

    name_space.add(wallet)
