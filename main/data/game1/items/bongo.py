from utils.relator              import NameFinder
from models.actors              import Target, TargetInfo
from readin.description_helpers import PlainTextContext, PlainTextDescription
from readin.utils               import sdg_from_parts

def add_to_name_space(name_space:NameFinder) -> None:
    sdg = sdg_from_parts(
        unbreakable_states=[name_space.get_from_id("visible",  "state")],
        state_graphs      =[name_space.get_from_id("takeable sg", "stategraph")],
        breakable_states  =[name_space.get_from_id("musical",  "state")],
        name_space        =name_space
    )

    bongo = Target(
        name="Bongo",
        description_context=PlainTextContext("a bongo"),
        description_strategy=PlainTextDescription(),
        target_info=TargetInfo(
            states=sdg,
        ),
        weight=5,
        value=3,
        size=1
    )

    name_space.add(bongo)
