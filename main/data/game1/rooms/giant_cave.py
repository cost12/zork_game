from models.actors              import Location, SingleEndPath
from utils.relator              import NameFinder
from readin.stand_in            import StandIn
from readin.description_helpers import Description, PlainTextContext, PlainTextDescription
from readin.restriction_helpers import Restriction, ItemStateRestriction, ItemStateContext, ItemPlacementContext, ItemPlacementRestriction

def add_to_name_space(name_space:NameFinder) -> None:
    northeast_path = SingleEndPath(
        name="Giant Cave Northeast Exit",
        description=Description[PlainTextContext](PlainTextContext("A passage leads northeast."), PlainTextDescription()),
        end=StandIn[Location]("beehive room", "location")
    )

    south_path = SingleEndPath(
        name="Giant Cave South Exit",
        description=Description[PlainTextContext](PlainTextContext("A distant hole in the stone room leads south."), PlainTextDescription()),
        end=StandIn[Location]("candlelit room", "location")
    )

    location = Location(
        name="Giant Cave",
        description=Description[PlainTextContext](PlainTextContext("You stand in a massive cave whose ceiling is nearly too tall to see. Bats screeches echo distantly. Guano coats most the walls."), PlainTextDescription()),
        paths={
            name_space.get_from_id('northeast', 'direction') : northeast_path,
            name_space.get_from_id('south',     'direction') : south_path
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
    name_space.add_many([south_path, northeast_path, location])
