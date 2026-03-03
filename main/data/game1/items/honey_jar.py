from utils.relator              import NameFinder
from models.actors              import Target, LocationDetail, ItemLimit, TargetInfo
from readin.description_helpers import PlainTextDescription, PlainTextContext, plain_text_description
from readin.utils               import sdg_from_parts
from readin.stand_in            import StandIn

def add_to_name_space(name_space:NameFinder) -> None:
    sdg = sdg_from_parts(
        unbreakable_states=[name_space.get_from_id("visible",   "state")],
        state_graphs      =[name_space.get_from_id("container sg", "stategraph"),
                            name_space.get_from_id("takeable sg", "stategraph")],
        name_space        =name_space
    )

    inside = LocationDetail(
        name="in",
        name_id="in honey jar",
        item_limit=ItemLimit(1, 1),
        #children=[StandIn("honey", "target")] TODO
    )

    jar = Target(
        name="honey jar",
        aliases=["jar"],
        description_context=PlainTextContext("a jar for honey"),
        description_strategy=PlainTextDescription(),
        #children=[inside], TODO
        weight=1,
        value=3,
        size=2,
        target_info=TargetInfo(
            states=sdg,
            state_responses={
                name_space.get_from_id("held",          "state") : plain_text_description("The jar is cool to the touch."),
                name_space.get_from_id("empty (state)", "state") : plain_text_description("The jar is empty."),
                name_space.get_from_id("broken",        "state") : plain_text_description("The jar shatters, rendering itself unusable. Nice going."),
            },
        ),
        item_responses={
            StandIn("honey", "target") : plain_text_description("The jar is full of honey."),
            StandIn("water", "target") : plain_text_description("The jar is full of water.")
        }
    )

    name_space.add_many([jar, inside])
