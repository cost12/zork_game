from utils.relator import NameFinder
from models.actors import Target, TargetInfo
from readin.description_helpers import PlainTextDescription, PlainTextContext, plain_text_description
from readin.utils import sdg_from_parts

def add_to_name_space(name_space:NameFinder) -> None:
    sdg = sdg_from_parts(
        unbreakable_states=[name_space.get_from_id("visible",   "state")],
        state_graphs      =[name_space.get_from_id("switch sg", "stategraph"),
                            name_space.get_from_id("takeable sg", "stategraph")],
        name_space        =name_space
    )

    lantern = Target(
        name="lantern",
        aliases=["lamp"],
        description_context=PlainTextContext("a small survival lantern"),
        description_strategy=PlainTextDescription(),
        weight=1,
        value=1,
        size=1,
        target_info=TargetInfo(
            states=sdg,
            state_responses={
                name_space.get_from_id("on",     "state") : plain_text_description("The lantern is on."),
                name_space.get_from_id("off",    "state") : plain_text_description("The lantern is off."),
                name_space.get_from_id("broken", "state") : plain_text_description("The lantern is broken and can't be turned on. Pity..."),
                name_space.get_from_id("held",   "state") : plain_text_description("The lantern is surprisingly light!")
            }
        )
    )

    name_space.add(lantern)
