from utils.relator              import NameFinder
from models.actors              import Target, LocationDetail, ItemLimit, TargetInfo
from readin.description_helpers import PlainTextDescription, PlainTextContext, plain_text_description
from readin.utils               import sdg_from_parts
from readin.stand_in            import StandIn
from readin.restriction_helpers import Restriction, ItemStateContext, ItemStateRestriction

def add_to_name_space(name_space:NameFinder) -> None:
    sdg = sdg_from_parts(
        unbreakable_states=[name_space.get_from_id("visible",   "state")],
        state_graphs      =[name_space.get_from_id("locked sg", "stategraph"),
                            name_space.get_from_id("container sg", "stategraph")],
        name_space        =name_space
    )

    inside = LocationDetail(
        name="in",
        name_id="in trunk",
        item_limit=ItemLimit(30, 100),
        visible_restrictions=[Restriction[ItemStateContext](ItemStateContext(StandIn("trunk", "target"), name_space.get_from_id("opened", "state"), "The trunk is closed."), ItemStateRestriction())],
        #children=[name_space.get_from_id("basketball", "target"), name_space.get_from_id("skateboard", "target")] TODO
    )

    on = LocationDetail(
        name="on",
        name_id="on trunk",
        item_limit=ItemLimit(20, 100),
        #children=[name_space.get_from_id("pepper jar", "target")] TODO
    )

    trunk = Target(
        name="trunk",
        description_context=PlainTextContext("an honest, squat trunk"),
        description_strategy=PlainTextDescription(),
        #children=[inside, on], TODO
        weight=100,
        value=3,
        size=30,
        target_info=TargetInfo(
            states=sdg,
            target_responses={
                name_space.get_from_id("take",  "action") : plain_text_description("The trunk's a bit too heavy for you to carry."),
                name_space.get_from_id("break", "action") : plain_text_description("Why would you want to do a thing like that?")
            },
            state_responses={
                name_space.get_from_id("opened",   "state") : plain_text_description("The trunk's lid squeaks open, revealing its contents."),
                name_space.get_from_id("closed",   "state") : plain_text_description("The trunk's lid slams shut dramatically."),
                name_space.get_from_id("unlocked", "state") : plain_text_description("The trunk's lock disengages with a satisfying click."),
                name_space.get_from_id("locked",   "state") : plain_text_description("You re-engage the trunk's lock."),
            }
        )
    )

    name_space.add_many([trunk, inside, on])
