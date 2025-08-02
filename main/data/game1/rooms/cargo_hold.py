from models.actors              import Location, SingleEndPath
from utils.relator              import NameFinder
from readin.stand_in            import StandIn
from readin.description_helpers import Description, PlainTextContext, PlainTextDescription

def add_to_name_space(name_space:NameFinder) -> None:
    north_path = SingleEndPath(
        name="Cargo Hold North Exit",
        description="Northwards, the train continues.",
        end=StandIn[Location]("Conductor's Car", "location")
    )

    south_path = SingleEndPath(
        name="Cargo Hold South Exit",
        description=Description[PlainTextContext](PlainTextContext("Another train car is to the south."), PlainTextDescription()),
        end=StandIn[Location]("Hallway", "location")
    )

    location = Location(
        name="Cargo Hold",
        description=Description[PlainTextContext](PlainTextContext("You are standing in a dark, musty shipping container. Its contents are long gone, and only a few piles of rust remain. You hear a shrill sliding melody playing through some hidden speakers."), PlainTextDescription()),
        paths={
            name_space.get_from_id('north', 'direction') : north_path,
            name_space.get_from_id('south', 'direction') : south_path
        }
    )
    name_space.add_many([north_path, south_path, location])
