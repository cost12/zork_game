from models.actors              import Location, SingleEndPath
from utils.relator              import NameFinder
from readin.stand_in            import StandIn
from readin.description_helpers import Description, PlainTextContext, PlainTextDescription
from readin.restriction_helpers import Restriction, ItemStateRestriction, ItemStateContext, ItemPlacementContext, ItemPlacementRestriction

def add_to_name_space(name_space:NameFinder) -> None:
    north_path = SingleEndPath(
        name="Riches Room North Exit",
        description=Description[PlainTextContext](PlainTextContext("A passage leads north."), PlainTextDescription()),
        end=StandIn[Location]("candlelit room", "location")
    )

    south_path = SingleEndPath(
        name="Riches Room South Exit",
        description=Description[PlainTextContext](PlainTextContext("A cement walkway goes to the south."), PlainTextDescription()),
        end=StandIn[Location]("parking lot", "location")
    )

    location = Location(
        name="Riches Room",
        description=Description[PlainTextContext](PlainTextContext("You stand at the edge of a large room full of treasure, riches beyond your wildest imagination. Gold, silver and platinum coins pile high, magical weapons glint and glow, enchanted scrolls sit amongst precious gemstones glimmering prismatically. On the floor is a simple mosaic depicting a hand holding a coin and an arrow pointing to a skull and crossbones. The message is clear: touch, and die."), PlainTextDescription()),
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
