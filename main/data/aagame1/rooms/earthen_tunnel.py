from models.actors              import Location, SingleEndPath
from utils.relator              import NameFinder
from readin.stand_in            import StandIn
from readin.description_helpers import Description, PlainTextContext, PlainTextDescription
from readin.restriction_helpers import Restriction, ItemStateRestriction, ItemStateContext, ItemPlacementContext, ItemPlacementRestriction

def add_to_name_space(name_space:NameFinder) -> None:
    north_path = SingleEndPath(
        name="Earthen Tunnel North Exit",
        description=Description[PlainTextContext](PlainTextContext("A passage slopes northwards."), PlainTextDescription()),
        end=StandIn[Location]("Garden", "location")
    )

    south_path = SingleEndPath(
        name="Earthen Tunnel South Exit",
        description=Description[PlainTextContext](PlainTextContext("A passage leads south."), PlainTextDescription()),
        end=StandIn[Location]("small cavern", "location")
    )

    location = Location(
        name="Earthen Tunnel",
        description=Description[PlainTextContext](PlainTextContext("You find yourself crouched in a squat earthen tunnel that runs north-south. The smells of minerals and decay fill your nostrils."), PlainTextDescription()),
        paths={
            name_space.get_from_id('north', 'direction') : north_path,
            name_space.get_from_id('south', 'direction') : south_path
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
        }
    )
    name_space.add_many([south_path, north_path, location])
