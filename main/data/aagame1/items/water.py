from utils.relator import NameFinder
from models.actors import Target
from models.response import StaticResponse
from readin.description_helpers import plain_text
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
        description=(plain_text, "water"),
        states=sdg,
        weight=1,
        value=1,
        size=1,
        target_responses={
            name_space.get_from_id("take", "action") : StaticResponse("You reach a hand into the water and attempt to grab it. Unsurprisingly this method is innefective and only leaves your hand slightly wet. I hope you weren't planning to drink this water.")
        }
    )

    name_space.add(water)
