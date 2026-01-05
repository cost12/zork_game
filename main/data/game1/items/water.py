from utils.relator import NameFinder
from models.actors import Target, TargetInfo
from readin.description_helpers import PlainTextDescription, PlainTextContext, plain_text_description
from readin.utils import sdg_from_parts

def add_to_name_space(name_space:NameFinder) -> None:
    sdg = sdg_from_parts(
        unbreakable_states=[name_space.get_from_id("visible", "state"),
                            name_space.get_from_id("edible",  "state"),
                            name_space.get_from_id("liquid",  "state")],
        name_space        =name_space
    )

    water = Target(
        name="water",
        description_context=PlainTextContext("water"),
        description_strategy=PlainTextDescription(),
        weight=1,
        value=1,
        size=1,
        target_info=TargetInfo(
            states=sdg,
            target_responses={
                name_space.get_from_id("take", "action") : plain_text_description("You reach a hand into the water and attempt to grab it. Unsurprisingly this method is innefective and only leaves your hand slightly wet. I hope you weren't planning to drink this water.")
            }
        )
    )

    name_space.add(water)
