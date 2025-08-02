from models.actors              import Location, SingleEndPath
from utils.relator              import NameFinder
from readin.stand_in            import StandIn
from readin.description_helpers import Description, PlainTextContext, PlainTextDescription
from readin.restriction_helpers import Restriction, ItemStateRestriction, ItemStateContext, ItemPlacementContext, ItemPlacementRestriction

def add_to_name_space(name_space:NameFinder) -> None:
    west_path = SingleEndPath(
        name="Crystal Cave West Exit",
        description=Description[PlainTextContext](PlainTextContext("A passage leads west"), PlainTextDescription()),
        end=StandIn[Location]("Greenhouse", "location")
    )

    south_path = SingleEndPath(
        name="Crystal Cave South Exit",
        description=Description[PlainTextContext](PlainTextContext("A passage leads south."), PlainTextDescription()),
        end=StandIn[Location]("Pool", "location")
    )

    location = Location(
        name="Crystal Cave",
        description=Description[PlainTextContext](PlainTextContext("You stand in a natural wonder, the center of a huge spherical geode. Gleaming crystals cover every surface, refracting light from every angle and showing your shattered reflection a thousand times over. Your breath is taken away by the overwhelming beauty."), PlainTextDescription()),
        paths={
            name_space.get_from_id('west',  'direction') : west_path,
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
    name_space.add_many([south_path, west_path, location])
