from utils.relator import NameFinder
from models.actors import Target
from models.response import StaticResponse
from readin.description_helpers import plain_text
from readin.utils import sdg_from_parts

def add_to_name_space(name_space:NameFinder) -> None:
    sdg = sdg_from_parts(
        unbreakable_states=[name_space.get_from_id("visible",   "state")],
        state_graphs      =[name_space.get_from_id("takeable",  "stategraph"),
                            name_space.get_from_id("flammable", "stategraph")],
        breakable_states  =[name_space.get_from_id("hangable",  "state")],
        name_space        =name_space
    )

    painting = Target(
        name="painting",
        aliases=["hercules"],
        description=(plain_text, "a medium-sized painting depictiong Hercules wrestling the Nemean Lion, gracefully rendered in romantic fashion"),
        states=sdg,
        weight=3,
        value=1,
        size=4,
        target_responses={
            name_space.get_from_id("hang", "action") : StaticResponse("The painting rests on the wall, proudly displayed")
        },
        state_responses={
            name_space.get_from_id("taken",  "state") : StaticResponse("You take the painting from its resting place, marveling at the detail from so close. Be careful!"),
            name_space.get_from_id("broken", "state") : StaticResponse("As a complete vandal, shitting on the annals of history, you destroy this priceless work of art.")
        }
    )

    name_space.add(painting)
