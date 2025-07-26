from utils.relator import NameFinder
from models.actors import Target, LocationDetail, ItemLimit
from readin.description_helpers import Description, StateDescription, StateContext
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
        id="in cabinet",
        item_limit=ItemLimit(20, 50),
        children=[StandIn("mason jar", "target"), StandIn("rusty fork", "target")],
        visible_requirements=Restriction[ItemStateContext](ItemStateContext(StandIn("cabinet", "target"), name_space.get_from_id("opened", "state"), "The cabinet is closed."), ItemStateRestriction())
    )

    cabinet = Target(
        name="cabinet",
        description=Description[StateContext](StateContext({
            name_space.get_from_id("open",   "state") : "an open cabinet",
            name_space.get_from_id("closed", "state") : "a closed cabinet"
        }), StateDescription()),
        states=sdg,
        children=[
            inside
        ],
        weight=5,
        value=3,
        size=1,
    )

    name_space.add_many([cabinet, inside])
