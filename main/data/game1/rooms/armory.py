from models.actors              import Location, LocationDetail, LocationInfo
from utils.relator              import NameFinder
from readin.description_helpers import PlainTextContext, PlainTextDescription, ContentsContext, ContentsDescription
from readin.restriction_helpers import Restriction, ItemStateRestriction, ItemStateContext, ItemPlacementContext, ItemPlacementRestriction

def add_to_name_space(name_space:NameFinder) -> None:
    rack = LocationDetail(
        name="rack",
        description_context=ContentsContext("Hanging on a well-worn wooden rack is", "An empty weapons rack hangs on the wall."),
        description_strategy=ContentsDescription(),
        #children=[StandIn("spear", "target"), StandIn("pitchfork", "target"), StandIn("sword", "target")] TODO
    )

    armory = Location(
        name="Armory",
        description_context=PlainTextContext("You stand in an old armory that once held many armaments and much armor. All that remains are a few neglected weapons. On the floor is a mosaic resembling an hourglass with both glass canisters cracked."),
        description_strategy=PlainTextDescription(),
        #children=[rack], TODO
        location_info=LocationInfo(
            action_restrictions={
                name_space.get_from_id("take", "action") : Restriction[ItemStateContext](
                    ItemStateContext(name_space.get_from_id("hourglass", "target"), name_space.get_from_id("broken", "state"), "As you move to place the item in your inventory, it turns to dust. As if guided by some ancient curse it slips through your fingers and reforms in it's previous location."), ItemStateRestriction()
                ),
                name_space.get_from_id("look", "action") : [
                    Restriction[ItemStateContext](
                        ItemStateContext(name_space.get_from_id("lantern", "target"), name_space.get_from_id("on", "state"), "You try to look, but you can't see a thing."), ItemStateRestriction()
                    ),
                    Restriction[ItemPlacementContext](
                        ItemPlacementContext(name_space.get_from_id("lantern", "target"), name_space.get_from_id("armory", "location"), "You try to look but you can't see a thing."), ItemPlacementRestriction()
                    )
                ]
            },
        )
    )

    name_space.add_many([rack, armory])
