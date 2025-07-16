from utils.relator import NameFinder
from models.actors import Target
from models.response import StaticResponse
from readin.description_helpers import plain_text
from readin.utils import sdg_from_parts

def add_to_name_space(name_space:NameFinder) -> None:
    sdg = sdg_from_parts(
        unbreakable_states=[name_space.get_from_id("visible",  "state")],
        state_graphs      =[name_space.get_from_id("takeable", "stategraph")],
        breakable_states  =[name_space.get_from_id("conductable",   "state")],
        name_space        =name_space
    )

    baton = Target(
        name="Baton",
        description=(plain_text, "an elegant conductor's baton, wrought from ivory"),
        states=sdg,
        weight=1,
        value=10,
        size=1,
        target_responses={
            name_space.get_from_id("take", "action")    : StaticResponse("This must have belonged to a prolific maestro, for you feel years of orchestral experience flowing through you"),
            name_space.get_from_id("conduct", "action") : StaticResponse("You hear a stunning Baritone sing operatically: 'One instrument, One Journey'. Or is it an Alto?")
        },
        state_responses={
            name_space.get_from_id("broken", "action")  : StaticResponse("Why oh why? You hear the echo of an audience groan as you snap the baton.")
        }
    )

    name_space.add(baton)