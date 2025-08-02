from models.actors              import Location, SingleEndPath
from utils.relator              import NameFinder
from readin.stand_in            import StandIn
from readin.description_helpers import Description, PlainTextContext, PlainTextDescription
from readin.restriction_helpers import Restriction, ItemStateRestriction, ItemStateContext, ItemPlacementContext, ItemPlacementRestriction

def add_to_name_space(name_space:NameFinder) -> None:
    any_path = SingleEndPath(
        name="Car Trunk Exit",
        description=Description[PlainTextContext](PlainTextContext("The garage is outside."), PlainTextDescription()),
        end=StandIn[Location]("Parking Lot", "location")
    )

    location = Location(
        name="Car Trunk",
        description=Description[PlainTextContext](PlainTextContext("For some reason, you are in the car's trunk. You have to curl up in order to fit. What an odd thing to do!"), PlainTextDescription()),
        paths={
            name_space.get_from_id('any', 'direction') : any_path
        },
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
    name_space.add_many([any_path, location])
