from models.actors              import Location, LocationInfo
from utils.relator              import NameFinder
from readin.description_helpers import PlainTextContext, PlainTextDescription
from readin.restriction_helpers import Restriction, ItemPlacementContext, ItemPlacementRestriction, ItemStateContext, ItemStateRestriction

def add_to_name_space(name_space:NameFinder) -> None:
    location = Location(
        name="Cold Room",
        description_context=PlainTextContext("You enter what feels like a blast chiller. Frost covers the walls and floor. Your breath forms a thick cloud in front of your face and you shiver violently. Embedded in the floor in front of the passage opposite your entrance it is a vent that must be the source of the cold."),
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

    name_space.add_many([location])
