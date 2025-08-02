from models.actors              import Location, SingleEndPath
from utils.relator              import NameFinder
from readin.stand_in            import StandIn
from readin.description_helpers import Description, PlainTextContext, PlainTextDescription

def add_to_name_space(name_space:NameFinder) -> None:
    north_path = SingleEndPath(
        name="Observation Car North Exit",
        description=Description[PlainTextContext](PlainTextContext("The train continues north."), PlainTextDescription()),
        end=StandIn[Location]("cargo hold", "location")
    )

    south_path = SingleEndPath(
        name="Observation Car South Exit",
        description=Description[PlainTextContext](PlainTextContext("The train continues south."), PlainTextDescription()),
        end=StandIn[Location]("Dining car", "location")
    )

    location = Location(
        name="Observation Car",
        description=Description[PlainTextContext](PlainTextContext("You are standing in a train whose walls and ceilings are entirely made of glass. In every direction you can see ocean stretching endlessly. A plucked flurry of a song plays."), PlainTextDescription()),
        paths={
            name_space.get_from_id('north', 'direction') : north_path,
            name_space.get_from_id('south', 'direction') : south_path
        }
    )
    name_space.add_many([south_path, north_path, location])
