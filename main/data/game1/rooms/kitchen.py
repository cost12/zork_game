from models.actors              import Location, SingleEndPath
from utils.relator              import NameFinder
from readin.stand_in            import StandIn
from readin.description_helpers import Description, PlainTextContext, PlainTextDescription

def add_to_name_space(name_space:NameFinder) -> None:
    north_path = SingleEndPath(
        name="Kitchen North Exit",
        description=Description[PlainTextContext](PlainTextContext("To the north is a doorway."), PlainTextDescription()),
        end=StandIn[Location]("hallway", "location")
    )

    west_path = SingleEndPath(
        name="Kitchen West Exit",
        description=Description[PlainTextContext](PlainTextContext("To the west is a doorway."), PlainTextDescription()),
        end=StandIn[Location]("den", "location")
    )

    location = Location(
        name="Kitchen",
        description=Description[PlainTextContext](PlainTextContext("You are standing in a modest kitchen. You hear a rush of footsteps in a nearby room."), PlainTextDescription()),
        paths={
            name_space.get_from_id('north', 'direction') : north_path,
            name_space.get_from_id('west',  'direction') : west_path
        },
        children=[
            name_space.get_from_id("cabinet",      "target"),
            name_space.get_from_id("stove",        "target"),
            name_space.get_from_id("kitchen sink", "target")
        ]
    )
    name_space.add_many([west_path, north_path, location])
