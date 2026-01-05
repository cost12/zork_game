from utils.relator import NameFinder
from models.actors import Target, TargetInfo
from readin.description_helpers import PlainTextDescription, PlainTextContext, plain_text_description
from readin.utils import sdg_from_parts

def add_to_name_space(name_space:NameFinder) -> None:
    sdg = sdg_from_parts(
        unbreakable_states=[name_space.get_from_id("visible",   "state")],
        state_graphs      =[name_space.get_from_id("flammable", "stategraph"),
                            name_space.get_from_id("takeable",  "stategraph")],
        breakable_states  =[name_space.get_from_id("readable",  "state")],
        name_space        =name_space
    )

    leaflet = Target(
        name="leaflet",
        description_context=PlainTextContext("a small handwritten leaflet"),
        description_strategy=PlainTextDescription(),
        weight=0.5,
        value=1,
        size=1,
        target_info=TargetInfo(
            states=sdg,
            target_responses={
                name_space.get_from_id("read", "action") : plain_text_description("Welcome to Thief: Level 1, a text-based adventure inspired by the OG, Zork. Explore a mysterious abandoned world as you quest to find your missing wallet and keys. Can you find them, and discover the grave secrets of this forsaken realm?")
            },
            state_responses={
                name_space.get_from_id("broken", "state") : plain_text_description("The leaflet is ripped to shreds"),
            }
        )
    )

    name_space.add(leaflet)
