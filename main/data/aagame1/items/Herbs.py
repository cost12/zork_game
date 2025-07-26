from utils.relator import NameFinder
from models.actors import Target
from models.response import StaticResponse
from readin.description_helpers import plain_text
from readin.utils import sdg_from_parts

def add_to_name_space(name_space:NameFinder) -> None:
    sdg = sdg_from_parts(
        unbreakable_states=[name_space.get_from_id("visible",       "state")],
        state_graphs      =[name_space.get_from_id("takeable",      "stategraph"),
                            name_space.get_from_id("flammable",     "stategraph"),
                            name_space.get_from_id("fragile_untie", "stategraph")],
        name_space        =name_space
    )

    herbs = Target(
        name="dried herbs",
        aliases=["herbs"],
        description=Description[PlainTextContext](PlainTextContext("a small, tightly packed bundle of herbs bound by a short length of hemp twine"), PlainTextDescription()),
        states=sdg,
        weight=1,
        value=1,
        size=1,
        target_responses={
            name_space.get_from_id("burn",  "action") : StaticResponse("With what?"),
            name_space.get_from_id("untie", "action") : StaticResponse("You untie the bundle. The hempen twine disintigrates at your touch, and the herbacious leaves fall to the ground, scattered. You cannot gather them.")
        },
        state_responses={
            name_space.get_from_id("broken", "state") : StaticResponse("You scatter the desicated leaves to the ground")
        }
    )

    name_space.add(herbs)
