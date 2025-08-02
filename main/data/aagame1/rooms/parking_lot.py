from models.actors              import Location, SingleEndPath, MultiEndPath, LocationDetail
from utils.relator              import NameFinder
from readin.stand_in            import StandIn
from readin.description_helpers import Description, PlainTextContext, PlainTextDescription, ContentsContext, ContentsDescription
from readin.restriction_helpers import Restriction, ItemStateRestriction, ItemStateContext, ItemPlacementContext, ItemPlacementRestriction

def add_to_name_space(name_space:NameFinder) -> None:
    north_path = MultiEndPath(
        name="Parking Lot North Exit",
        description=Description[PlainTextContext](PlainTextContext("An exit ramp leads to the north."), PlainTextDescription()),
        end=StandIn[Location]("riches room", "location"),
        multi_end={
            name_space.get_from_id("triangle", "target") : StandIn("theatre stage", "location")
        }
    )

    in_trunk_path = SingleEndPath(
        name="Parking Lot Trunk Exit",
        description=Description[PlainTextContext](PlainTextContext(None), PlainTextDescription()),
        end=StandIn[Location]("Car trunk", "location")
    )

    in_car_path = SingleEndPath(
        name="Parking Lot Car Exit",
        description=Description[PlainTextContext](PlainTextContext("The driver's door."), PlainTextDescription()),
        end=StandIn[Location]("driver's seat", "location")
    )

    child = LocationDetail(
        name="in trunk",
        description=Description[ContentsContext](ContentsContext("Nestled in the corner of the trunk is", "The trunk is dissapointingly empty"), ContentsDescription()),
        children=[name_space.get_from_id("fuzzy jacket", "target")],
        visible_requirements=[
            Restriction[ItemStateContext](ItemStateContext(name_space.get_from_id("trunk door", "target"), name_space.get_from_id("opened", "state"), "You can't see into the trunk."), ItemStateRestriction())
        ]
    )

    location = Location(
        name="Parking Lot",
        description=Description[PlainTextContext](PlainTextContext("You are standing in a large underground parking lot dotted with square concrete columns. A single car is parked, lonesomely covered in a layer of dust."), PlainTextDescription()),
        paths={
            name_space.get_from_id('north',    'direction') : north_path,
            name_space.get_from_id('in trunk', 'direction') : in_trunk_path,
            name_space.get_from_id("in car",   "direction") : in_car_path
        },
        children=[child, name_space.get_from_id("orge", "actor")],
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
    name_space.add_many([child, in_trunk_path, in_car_path, north_path, location])
