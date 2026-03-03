from utils.relator import NameFinder
from models.actors import Target, TargetInfo
from readin.description_helpers import PlainTextDescription, PlainTextContext, plain_text_description
from readin.utils import sdg_from_parts

def add_to_name_space(name_space:NameFinder) -> None:
    sdg = sdg_from_parts(
        unbreakable_states=[name_space.get_from_id("visible",  "state")],
        state_graphs      =[name_space.get_from_id("takeable sg", "stategraph")],
        breakable_states  =[name_space.get_from_id("sharp",    "state")],
        name_space        =name_space
    )

    pitchfork = Target(
        name="pitchfork",
        description_context=PlainTextContext("a long-handled pitchfork with three sharp tines"),
        description_strategy=PlainTextDescription(),
        weight=3,
        value=3,
        size=5,
        target_info=TargetInfo(
            states=sdg,
            state_responses={
                name_space.get_from_id("held",   "state") : plain_text_description("You feel many hours of farm work in the wooden handle's grain"),
                name_space.get_from_id("broken", "state") : plain_text_description("Seems odd. You break the handle in two.")
            }
        )
    )

    name_space.add(pitchfork)
