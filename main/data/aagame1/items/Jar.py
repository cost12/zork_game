from utils.relator              import NameFinder
from models.actors              import Target, LocationDetail, ItemLimit
from models.response            import StaticResponse
from readin.description_helpers import plain_text
from readin.utils               import sdg_from_parts
from readin.stand_in            import StandIn

def add_to_name_space(name_space:NameFinder) -> None:
    sdg = sdg_from_parts(
        unbreakable_states=[name_space.get_from_id("visible",   "state")],
        state_graphs      =[name_space.get_from_id("container", "stategraph"),
                            name_space.get_from_id("takeable",  "stategraph")],
        name_space        =name_space
    )

    jar = Target(
        name="mason jar",
        aliases=["jar"],
        description=(plain_text, "a smudged and empty mason jar"),
        states=sdg,
        children=[
            LocationDetail(
                name="in",
                item_limit=ItemLimit(1, 1)
            )
        ],
        weight=1,
        value=3,
        size=2,
        state_responses={
            name_space.get_from_id("taken",         "state") : StaticResponse("The jar is cool to the touch."),
            name_space.get_from_id("full",          "state") : StaticResponse("The jar is full."),
            name_space.get_from_id("empty (state)", "state") : StaticResponse("The jar is empty."),
            name_space.get_from_id("broken",        "state") : StaticResponse("The jar shatters, rendering itself unusable. Nice going."),
        },
        item_responses={
            StandIn("honey",   "target") : StaticResponse("The jar is full of honey."),
            StandIn("water",   "target") : StaticResponse("The jar is full of water."),
            StandIn("peppers", "target") : StaticResponse("The jar is full of peppers.")
        }
    )

    name_space.add(jar)
