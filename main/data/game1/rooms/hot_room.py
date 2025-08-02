from models.actors              import Location, SingleEndPath
from utils.relator              import NameFinder
from readin.stand_in            import StandIn
from readin.description_helpers import Description, PlainTextContext, PlainTextDescription
from readin.restriction_helpers import Restriction, ItemStateRestriction, ItemStateContext, ItemPlacementContext, ItemPlacementRestriction

def add_to_name_space(name_space:NameFinder) -> None:
    northeast_path = SingleEndPath(
        name="Hot Room Northeast Exit",
        description=Description[PlainTextContext](PlainTextContext("A passage leads northeast."), PlainTextDescription()),
        end=StandIn[Location]("theatre stage", "location")
    )

    south_path = SingleEndPath(
        name="Hot Room South Exit",
        description=Description[PlainTextContext](PlainTextContext("A passage leads south, eminating some contionuous noise."), PlainTextDescription()),
        end=StandIn[Location]("conductor's car", "location")
    )

    location = Location(
        name="Hot Room",
        description=Description[PlainTextContext](PlainTextContext("You are standing in a room that is unbelievably hot, the air shimmering, rich with energy. In the center of the narrow room lies a vent that must be the source of the heat."), PlainTextDescription()),
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
