from utils.relator              import NameFinder
from models.actors              import Target
from models.response            import StaticResponse
from readin.description_helpers import plain_text
from readin.utils               import sdg_from_parts

def add_to_name_space(name_space:NameFinder) -> None:
    sdg = sdg_from_parts(
        unbreakable_states=[name_space.get_from_id("visible",  "state")],
        state_graphs      =[name_space.get_from_id("takeable", "stategraph")],
        breakable_states  =[name_space.get_from_id("musical",  "state")],
        name_space        =name_space
    )

    whistle = Target(
        name="slide whistle",
        aliases=["whistle"],
        description=(plain_text, "a slide whistle which, although it is a simple toy, posesses an attractive potential for unforseen elevation and unlikely craft"),
        states=sdg,
        weight=2,
        value=10,
        size=1,
        target_responses={
            name_space.get_from_id("play",  "action") : StaticResponse("You produce a few shrill, slippery notes. It sounds niether great, nor horrible, evoking little emotion.")
        },
        state_responses={
            name_space.get_from_id("held",   "state") : StaticResponse("The whistle feels less flimsy than you expected."),
            name_space.get_from_id("broken", "state") : StaticResponse("Bullishly, you rend the slide whistle into mishapen pieces.")
        }
    )

    name_space.add(whistle)
