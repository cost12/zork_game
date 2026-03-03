from utils.relator              import NameFinder
from models.actors              import Target, LocationDetail, ItemLimit, TargetInfo
from readin.description_helpers import PlainTextDescription, PlainTextContext, plain_text_description
from readin.utils               import sdg_from_parts
#from readin.stand_in            import StandIn

def add_to_name_space(name_space:NameFinder) -> None:
    sdg = sdg_from_parts(
        unbreakable_states=[name_space.get_from_id("visible",   "state")],
        state_graphs      =[name_space.get_from_id("container sg", "stategraph")],
        breakable_states  =[name_space.get_from_id("breakable sg", "stategraph")],
        name_space        =name_space
    )

    on = LocationDetail(
        name="on",
        name_id="on plate",
        item_limit=ItemLimit(1, 1),
        #children=[StandIn("meal", "target")] TODO
    )

    plate = Target(
        name="plate",
        description_context=PlainTextContext("a simple clay plate"),
        description_strategy=PlainTextDescription(),
        #children=[on], TODO
        weight=2,
        value=1,
        size=1,
        target_info=TargetInfo(
            states=sdg,
            state_responses={
                name_space.get_from_id("held",   "state") : plain_text_description("You the plate, only getting a little food on your hand."),
                name_space.get_from_id("broken", "state") : plain_text_description("The plate shatters and is useless."),
            }
        )
    )

    name_space.add_many([plate, on])
