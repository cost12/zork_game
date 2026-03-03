from utils.relator              import NameFinder
from models.actors              import Target, TargetInfo
from readin.description_helpers import PlainTextDescription, PlainTextContext, plain_text_description
from readin.utils               import sdg_from_parts

def add_to_name_space(name_space:NameFinder) -> None:
    sdg = sdg_from_parts(
        unbreakable_states=[name_space.get_from_id("visible",  "state"),
                            name_space.get_from_id("musical",  "state")],
        state_graphs      =[name_space.get_from_id("takeable sg", "stategraph")],
        name_space        =name_space
    )

    triangle = Target(
        name="triangle",
        description_context=PlainTextContext("a small metal triangle"),
        description_strategy=PlainTextDescription(),
        weight=2,
        value=10,
        size=1,
        target_info=TargetInfo(
            states=sdg,
            target_responses={
                name_space.get_from_id("play",  "action") : plain_text_description("It doesn't take much to be good at the triangle, and man are you a prodigy. Its high note rings out."),
                name_space.get_from_id("break", "action") : plain_text_description("The triangle is a slippery little bugger and you fuund yourself unable to destroy it.")
            },
            state_responses={
                name_space.get_from_id("held",   "state") : plain_text_description("The metal is cool to the touch.")
            }
        )
    )

    name_space.add(triangle)
