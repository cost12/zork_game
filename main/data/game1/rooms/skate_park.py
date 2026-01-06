from models.actors              import Location, LocationInfo
from utils.relator              import NameFinder
from readin.description_helpers import PlainTextContext, PlainTextDescription
from readin.restriction_helpers import Restriction, ItemStateRestriction, ItemStateContext, ItemPlacementContext, ItemPlacementRestriction

def add_to_name_space(name_space:NameFinder) -> None:
    location = Location(
        name="Skate Park",
        description_context=PlainTextContext("You stand at the top of a halfpipe at one edge of a small yet complex skate park. Graffiti covers the concrete walls and much of the undulating ground. A poster of Tony Hawk adorns one wall."),
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
        )
    )

    name_space.add_many([location])
