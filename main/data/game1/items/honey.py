from utils.relator import NameFinder
from models.actors import Target, TargetInfo
from readin.description_helpers import PlainTextDescription, PlainTextContext
from readin.utils import sdg_from_parts

def add_to_name_space(name_space:NameFinder) -> None:
    sdg = sdg_from_parts(
        unbreakable_states=[name_space.get_from_id("visible",  "state"),
                            name_space.get_from_id("edible",   "state")],
        state_graphs      =[name_space.get_from_id("takeable sg", "stategraph")],
        name_space        =name_space
    )

    honey = Target(
        name="honey",
        description_context=PlainTextContext("a bit of honey"),
        description_strategy=PlainTextDescription(),
        target_info=TargetInfo(
            states=sdg,
        ),
        weight=1,
        value=1,
        size=1,
    )

    name_space.add(honey)
