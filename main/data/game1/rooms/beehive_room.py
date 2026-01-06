from models.actors              import Location, LocationDetail, LocationInfo
from utils.relator              import NameFinder
from readin.description_helpers import PlainTextContext, PlainTextDescription, ContentsContext, ContentsDescription
from readin.restriction_helpers import Restriction, ItemStateRestriction, ItemStateContext, ItemPlacementContext, ItemPlacementRestriction

def add_to_name_space(name_space:NameFinder) -> None:
    child = LocationDetail(
        name="toilet",
        description_context=ContentsContext("Dripping from a large, intricate beehive is", "A large beehive buzzes with busy energy."),
		description_strategy=ContentsDescription(),
        #children=[StandIn("honey", "target")] TODO
    )

    location = Location(
        name="Beehive Room",
        description_context=PlainTextContext("You enter an odd, hexagonal room and immediately hear a loud buzzing sound. Bees fill the room, their hive in a corner to the east, dripping with honey. Passages are placed on each of the six gray concrete walls."),
		description_strategy=PlainTextDescription(),
        #children=[child, name_space.get_from_id("bear", "target")], TODO
        location_info=LocationInfo(
            action_restrictions={
                name_space.get_from_id("look", "action") : [
                    Restriction[ItemStateContext](
                        ItemStateContext(name_space.get_from_id("lantern", "target"), name_space.get_from_id("on", "state"), "You try to look, but you can't see a thing."), ItemStateRestriction()
                    ),
                    Restriction[ItemPlacementContext](
                        ItemPlacementContext(name_space.get_from_id("lantern", "target"), name_space.get_from_id("armory", "location"), "You try to look but you can't see a thing."), ItemPlacementRestriction()
                    )
                ]
            },
        ),
    )

    name_space.add_many([child, location])
