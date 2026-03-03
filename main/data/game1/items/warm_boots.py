from utils.relator import NameFinder
from models.actors import Target, TargetInfo
from readin.description_helpers import PlainTextDescription, PlainTextContext, plain_text_description
from readin.utils import sdg_from_parts

def add_to_name_space(name_space:NameFinder) -> None:
    sdg = sdg_from_parts(
        unbreakable_states=[name_space.get_from_id("visible",   "state")],
        state_graphs      =[name_space.get_from_id("takeable sg", "stategraph"),
                            name_space.get_from_id("wearable sg", "stategraph")],
        name_space        =name_space
    )

    boots = Target(
        name="warm boots",
        aliases=["boots", "hiking boots", "shoes"],
        description_context=PlainTextContext("a pair of hefty hiking boots"),
        description_strategy=PlainTextDescription(),
        weight=5,
        value=3,
        size=1,
        target_info=TargetInfo(
            states=sdg,
            target_responses={
                name_space.get_from_id("break",   "action") : plain_text_description("You tear at the boots, but their construction is such that you do little damage.")
            },
            state_responses={
                name_space.get_from_id("held",     "state") : plain_text_description("You take the hefty boots."),
                name_space.get_from_id("worn",     "state") : plain_text_description("The boots are a little stiff but feel highly protective against all pernicious elements"),
                name_space.get_from_id("wearable", "state") : plain_text_description("You take the boots off, revealing your bare, rough, gnarled feet."),
            }
        )
    )

    name_space.add(boots)
