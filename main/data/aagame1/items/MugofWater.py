from utils.relator              import NameFinder
from models.actors              import Target, LocationDetail, ItemLimit
from models.response            import StaticResponse, ContentsWithStateResponse
from readin.description_helpers import contents_text
from readin.utils               import sdg_from_parts
from readin.stand_in            import StandIn

def add_to_name_space(name_space:NameFinder) -> None:
    sdg = sdg_from_parts(
        unbreakable_states=[name_space.get_from_id("visible",   "state")],
        state_graphs      =[name_space.get_from_id("container", "stategraph"),
                            name_space.get_from_id("takeable",  "stategraph")],
        name_space        =name_space
    )

    mug = Target(
        name="mug",
        description=(contents_text, ("an empty ceramic mug", "a small ceramic mug full of")),
        states=sdg,
        children=[
            LocationDetail(
                name="in",
                item_limit=ItemLimit(1, 1),
                children=[StandIn("water", "target")]
            )
        ],
        weight=1,
        value=1,
        size=1,
        target_responses={
            name_space.get_from_id("pour", "action") : ContentsWithStateResponse(StandIn("mug", "target"), {name_space.get_from_id("liquid", "state") : "You empty the mug's contents, making a bit of a mess..."}, default="You turn the mug upside down, but nothing comes out.")
        },
        state_responses={
            name_space.get_from_id("taken",  "state") : ContentsWithStateResponse(StandIn("mug", "target"), {name_space.get_from_id("liquid", "state") : "You take the mug. Be fareful not to slosh!"}, default="You take the mug."),
            name_space.get_from_id("broken", "state") : StaticResponse("The mug is broken and can't be put back together again. Pity..."),
        },
        item_responses={
            StandIn("honey",   "target") : StaticResponse("The mug is full of honey."),
            StandIn("water",   "target") : StaticResponse("The mug is full of water."),
            StandIn("peppers", "target") : StaticResponse("The mug is full of peppers. Ew.")
        }
    )

    name_space.add(mug)
