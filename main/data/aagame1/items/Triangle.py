from utils.relator              import NameFinder
from models.actors              import Target
from models.response            import StaticResponse
from readin.description_helpers import plain_text
from readin.utils               import sdg_from_parts

def add_to_name_space(name_space:NameFinder) -> None:
    sdg = sdg_from_parts(
        unbreakable_states=[name_space.get_from_id("visible",  "state"),
                            name_space.get_from_id("musical",  "state")],
        state_graphs      =[name_space.get_from_id("takeable", "stategraph")],
        name_space        =name_space
    )

    triangle = Target(
        name="triangle",
        description=(plain_text, "a small metal triangle"),
        states=sdg,
        weight=2,
        value=10,
        size=1,
        target_responses={
            name_space.get_from_id("play",  "action") : StaticResponse("It doesn't take much to be good at the triangle, and man are you a prodigy. Its high note rings out."),
            name_space.get_from_id("break", "action") : StaticResponse("The triangle is a slippery little bugger and you fuund yourself unable to destroy it.")
        },
        state_responses={
            name_space.get_from_id("taken",  "state") : StaticResponse("The metal is cool to the touch.")
        }
    )

    name_space.add(triangle)
