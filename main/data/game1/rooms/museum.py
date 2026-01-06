from models.actors              import Location, LocationDetail, LocationInfo
from utils.relator              import NameFinder
from readin.description_helpers import PlainTextContext, PlainTextDescription, ContentsContext, ContentsDescription
from readin.restriction_helpers import Restriction, ItemPlacementContext, ItemPlacementRestriction, ItemStateContext, ItemStateRestriction

def add_to_name_space(name_space:NameFinder) -> None:
    child = LocationDetail(
        name="wall",
        description_context=ContentsContext("Hanging alone on the desolate walls is ", None),
		description_strategy=ContentsDescription(),
        #children=[name_space.get_from_id("hercules", "target")] TODO
    )

    location = Location(
        name="Museum Gallery",
        description_context=PlainTextContext("You are standing at the edge of a glorious museum gallery. The walls are gilded and enshrined with curlicue Rococo Era filigree. The walls are sadly bare."),
		description_strategy=PlainTextDescription(),
        #children=[child], TODO
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
        )
    )

    name_space.add_many([child, location])
