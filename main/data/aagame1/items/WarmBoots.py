from utils.relator import NameFinder
from models.actors import Target
from models.response import StaticResponse
from readin.description_helpers import plain_text
from readin.utils import sdg_from_parts

def add_to_name_space(name_space:NameFinder) -> None:
    sdg = sdg_from_parts(
        unbreakable_states=[name_space.get_from_id("visible",   "state")],
        state_graphs      =[name_space.get_from_id("takeable",  "stategraph"),
                            name_space.get_from_id("wearable",  "stategraph")],
        name_space        =name_space
    )

    boots = Target(
        name="warm boots",
        aliases=["boots", "hiking boots", "shoes"],
        description=(plain_text, "a pair of hefty hiking boots"),
        states=sdg,
        weight=5,
        value=3,
        size=1,
        target_responses={
            name_space.get_from_id("break",   "action") : StaticResponse("You tear at the boots, but their construction is such that you do little damage.")
        },
        state_responses={
            name_space.get_from_id("taken",    "state") : StaticResponse("You take the hefty boots."),
            name_space.get_from_id("worn",     "state") : StaticResponse("The boots are a little stiff but feel highly protective against all pernicious elements"),
            name_space.get_from_id("wearable", "state") : StaticResponse("You take the boots off, revealing your bare, rough, gnarled feet."),
        }
    )

    name_space.add(boots)
