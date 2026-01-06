from models.actors              import Location, LocationDetail, LocationInfo
from utils.relator              import NameFinder
from readin.description_helpers import PlainTextContext, PlainTextDescription, ContentsContext, ContentsDescription
from readin.restriction_helpers import Restriction, ItemStateRestriction, ItemStateContext, ItemPlacementContext, ItemPlacementRestriction

def add_to_name_space(name_space:NameFinder) -> None:
    child = LocationDetail(
        name="in trunk",
        description_context=ContentsContext("Nestled in the corner of the trunk is", "The trunk is dissapointingly empty"),
		description_strategy=ContentsDescription(),
        visible_restrictions=[
            Restriction[ItemStateContext](ItemStateContext(name_space.get_from_id("trunk door", "target"), name_space.get_from_id("opened", "state"), "You can't see into the trunk."), ItemStateRestriction())
        ]
    )

    location = Location(
        name="Parking Lot",
        description_context=PlainTextContext("You are standing in a large underground parking lot dotted with square concrete columns. A single car is parked, lonesomely covered in a layer of dust."),
		description_strategy=PlainTextDescription(),
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
