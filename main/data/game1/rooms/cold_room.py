from models.actors              import Location, SingleEndPath
from utils.relator              import NameFinder
from readin.stand_in            import StandIn
from readin.description_helpers import Description, PlainTextContext, PlainTextDescription
from readin.restriction_helpers import Restriction, ItemPlacementContext, ItemPlacementRestriction, ItemStateContext, ItemStateRestriction

def add_to_name_space(name_space:NameFinder) -> None:
    north_path = SingleEndPath(
        name="Cold Room North Exit",
        description=Description[PlainTextContext](PlainTextContext("A small passage leads north."), PlainTextDescription()),
        end=StandIn[Location]("south of tight pass", "location")
    )

    south_path = SingleEndPath(
        name="Cold Room South Exit",
        description=Description[PlainTextContext](PlainTextContext("An earthen passage leads south."), PlainTextDescription()),
        end=StandIn[Location]("bear's den", "location")
    )

    location = Location(
        name="Cold Room",
        description=Description[PlainTextContext](PlainTextContext("You enter what feels like a blast chiller. Frost covers the walls and floor. Your breath forms a thick cloud in front of your face and you shiver violently. Embedded in the floor in front of the passage opposite your entrance it is a vent that must be the source of the cold."), PlainTextDescription()),
        paths={
            name_space.get_from_id('north', 'direction') : north_path,
            name_space.get_from_id('south', 'direction') : south_path
        },
        children=[name_space.get_from_id("trunk", "target")],
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
    name_space.add_many([north_path, south_path, location])
