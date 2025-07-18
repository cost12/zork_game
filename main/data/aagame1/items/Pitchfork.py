from utils.relator import NameFinder
from models.actors import Target
from models.response import StaticResponse
from readin.description_helpers import plain_text
from readin.utils import sdg_from_parts

def add_to_name_space(name_space:NameFinder) -> None:
    sdg = sdg_from_parts(
        unbreakable_states=[name_space.get_from_id("visible",  "state")],
        state_graphs      =[name_space.get_from_id("takeable", "stategraph")],
        breakable_states  =[name_space.get_from_id("sharp",    "state")],
        name_space        =name_space
    )

    pitchfork = Target(
        name="pitchfork",
        description=(plain_text, "a long-handled pitchfork with three sharp tines"),
        states=sdg,
        weight=3,
        value=3,
        size=5,
        state_responses={
            name_space.get_from_id("taken",  "state") : StaticResponse("You feel many hours of farm work in the wooden handle's grain"),
            name_space.get_from_id("broken", "state") : StaticResponse("Seems odd. You break the handle in two.")
        }
    )

    name_space.add(pitchfork)
