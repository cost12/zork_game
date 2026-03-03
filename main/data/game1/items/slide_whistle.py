from utils.relator              import NameFinder
from models.actors              import Target, TargetInfo
from readin.description_helpers import PlainTextDescription, PlainTextContext, plain_text_description
from readin.utils               import sdg_from_parts

def add_to_name_space(name_space:NameFinder) -> None:
    sdg = sdg_from_parts(
        unbreakable_states=[name_space.get_from_id("visible",  "state")],
        state_graphs      =[name_space.get_from_id("takeable sg", "stategraph")],
        breakable_states  =[name_space.get_from_id("musical",  "state")],
        name_space        =name_space
    )

    whistle = Target(
        name="slide whistle",
        aliases=["whistle"],
        description_context=PlainTextContext("a slide whistle which, although it is a simple toy, posesses an attractive potential for unforseen elevation and unlikely craft"),
        description_strategy=PlainTextDescription(),
        weight=2,
        value=10,
        size=1,
        target_info=TargetInfo(
        states=sdg,
                target_responses={
                name_space.get_from_id("play",  "action") : plain_text_description("You produce a few shrill, slippery notes. It sounds niether great, nor horrible, evoking little emotion.")
            },
            state_responses={
                name_space.get_from_id("held",   "state") : plain_text_description("The whistle feels less flimsy than you expected."),
                name_space.get_from_id("broken", "state") : plain_text_description("Bullishly, you rend the slide whistle into mishapen pieces.")
            }
        )
    )

    name_space.add(whistle)
