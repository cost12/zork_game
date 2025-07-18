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

    spear = Target(
        name="spear",
        description=(plain_text, "a dope-ass long spear with a tuft to catch the blood of your foes"),
        states=sdg,
        weight=3,
        value=3,
        size=5,
        state_responses={
            name_space.get_from_id("taken",  "state") : StaticResponse("The spear fills you with a sense of confidence and competence. What a rush!"),
            name_space.get_from_id("broken", "state") : StaticResponse("Seems odd. You break the handle in two.")
        }
    )

    name_space.add(spear)
