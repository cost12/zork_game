from models.actors              import Location, SingleEndPath
from utils.relator              import NameFinder
from readin.stand_in            import StandIn
from readin.description_helpers import Description, PlainTextContext, PlainTextDescription
from readin.restriction_helpers import Restriction, ItemStateRestriction, ItemStateContext, ItemPlacementContext, ItemPlacementRestriction

def add_to_name_space(name_space:NameFinder) -> None:
    north_path = SingleEndPath(
        name="Small Cavern North Exit",
        description=Description[PlainTextContext](PlainTextContext("A narrow tunnel leads to the north."), PlainTextDescription()),
        end=StandIn[Location]("earthen tunnel", "location")
    )

    south_path = SingleEndPath(
        name="Small Cavern South Exit",
        description=Description[PlainTextContext](PlainTextContext("Amidst dripping stalagmites, a sturdy wooden door is installed to the south."), PlainTextDescription()),
        end=StandIn[Location]("beehive room", "location")
    )

    location = Location(
        name="Small Cavern",
        description=Description[PlainTextContext](PlainTextContext("You enter a small oblong cavern with rocky walls. A strange fragrant smell wafts through the overpowering odor of bat guano."), PlainTextDescription()),
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
