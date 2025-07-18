from utils.relator              import NameFinder
from models.actors              import Target, LocationDetail, ItemLimit
from models.response            import StaticResponse
from readin.description_helpers import plain_text
from readin.utils               import sdg_from_parts
from readin.stand_in            import StandIn
from readin.restriction_helpers import item_state_restriction

def add_to_name_space(name_space:NameFinder) -> None:
    sdg = sdg_from_parts(
        unbreakable_states=[name_space.get_from_id("visible",   "state")],
        state_graphs      =[name_space.get_from_id("locked", "stategraph"),
                            name_space.get_from_id("container",  "stategraph")],
        name_space        =name_space
    )

    inside = LocationDetail(
        name="in",
        id="in trunk",
        item_limit=ItemLimit(30, 100),
        visible_requirements=(
            item_state_restriction,
            (StandIn("trunk", "target"), name_space.get_from_id("opened", "state"), "The trunk is closed.")
        ),
        children=[
            name_space.get_from_id("basketball", "target"),
            name_space.get_from_id("skateboard", "target")
        ]
    )

    on = LocationDetail(
        name="on",
        id="on trunk",
        item_limit=ItemLimit(20, 100),
        children=[
            name_space.get_from_id("jar of peppers", "target")
        ]
    )

    trunk = Target(
        name="trunk",
        description=(plain_text, "an honest, squat trunk"),
        states=sdg,
        children=[
            inside,
            on
        ],
        weight=100,
        value=3,
        size=30,
        target_responses={
            name_space.get_from_id("take",  "action") : StaticResponse("The trunk's a bit too heavy for you to carry."),
            name_space.get_from_id("break", "action") : StaticResponse("Why would you want to do a thing like that?")
        },
        state_responses={
            name_space.get_from_id("opened",   "state") : StaticResponse("The trunk's lid squeaks open, revealing its contents."),
            name_space.get_from_id("closed",   "state") : StaticResponse("The trunk's lid slams shut dramatically."),
            name_space.get_from_id("unlocked", "state") : StaticResponse("The trunk's lock disengages with a satisfying click."),
            name_space.get_from_id("locked",   "state") : StaticResponse("You re-engage the trunk's lock."),
        }
    )

    name_space.add_many([trunk, inside, on])
