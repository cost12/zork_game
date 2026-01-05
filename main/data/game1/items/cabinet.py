from utils.relator import NameFinder
from models.actors import Target, LocationDetail, ItemLimit, TargetInfo
from readin.description_helpers import StateDescription, StateContext
from readin.restriction_helpers import Restriction, ItemStateRestriction, ItemStateContext
from readin.utils import sdg_from_parts
from readin.stand_in import StandIn

def add_to_name_space(name_space:NameFinder) -> None:
    sdg = sdg_from_parts(
        unbreakable_states=[name_space.get_from_id("visible",    "state")],
        state_graphs      =[name_space.get_from_id("open_close", "stategraph")],
        name_space        =name_space
    )

    inside = LocationDetail(
        name="in",
        name_id="in cabinet",
        item_limit=ItemLimit(20, 50),
        #children=[StandIn("mason jar", "target"), StandIn("rusty fork", "target")], TODO
        visible_restrictions=Restriction[ItemStateContext](ItemStateContext(StandIn("cabinet", "target"), name_space.get_from_id("opened", "state"), "The cabinet is closed."), ItemStateRestriction())
    )

    cabinet = Target(
        name="cabinet",
        description_context=StateContext({
            name_space.get_from_id("open",   "state") : "an open cabinet",
            name_space.get_from_id("closed", "state") : "a closed cabinet"
        }),
        description_strategy=StateDescription(),
        target_info=TargetInfo(
            states=sdg,
        ),
        #children=[inside], TODO
        weight=5,
        value=3,
        size=1,
    )

    name_space.add_many([cabinet, inside])
