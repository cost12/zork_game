from utils.relator              import NameFinder
from models.actors              import Target, LocationDetail, ItemLimit
from models.response            import StaticResponse
from readin.description_helpers import plain_text
from readin.utils               import sdg_from_parts
from readin.stand_in            import StandIn

def add_to_name_space(name_space:NameFinder) -> None:
    sdg = sdg_from_parts(
        unbreakable_states=[name_space.get_from_id("visible",   "state")],
        state_graphs      =[name_space.get_from_id("container", "stategraph")],
        breakable_states  =[name_space.get_from_id("breakable",  "stategraph")],
        name_space        =name_space
    )

    on = LocationDetail(
        name="on",
        id="on plate",
        item_limit=ItemLimit(1, 1),
        children=[StandIn("meal", "target")]
    )

    plate = Target(
        name="plate",
        description=(plain_text, "a simple clay plate"),
        states=sdg,
        children=[
            on
        ],
        weight=2,
        value=1,
        size=1,
        state_responses={
            name_space.get_from_id("held",   "state") : StaticResponse("You the plate, only getting a little food on your hand."),
            name_space.get_from_id("broken", "state") : StaticResponse("The plate shatters and is useless."),
        }
    )

    name_space.add_many([plate, on])
