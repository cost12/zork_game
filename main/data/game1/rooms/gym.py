from models.actors              import Location, LocationDetail, LocationInfo
from utils.relator              import NameFinder
from readin.description_helpers import PlainTextContext, PlainTextDescription, ContentsContext, ContentsDescription
from readin.restriction_helpers import Restriction, ItemPlacementContext, ItemPlacementRestriction, ItemStateContext, ItemStateRestriction

def add_to_name_space(name_space:NameFinder) -> None:
    child = LocationDetail(
        name="rack",
        description_context=ContentsContext("Sitting on a simple and sturdy rack is", "A small pyramid-shamed weight rack stands empty before the poster of Arnold."),
		description_strategy=ContentsDescription(),
        #children=[name_space.get_from_id("weights", "target")] TODO
    )

    location = Location(
        name="Gym",
        description_context=PlainTextContext("You are standing in a vintage-feeling gymnasium that feels strangely familiar. On one end is a basketball hoop and a weight rack at the opposite end. Behind the weight rack is a poster of Arnold Schwarzeneger holding up three fingers."),
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
            }
        )
    )

    name_space.add_many([child, location])
