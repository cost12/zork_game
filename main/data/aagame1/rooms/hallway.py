from models.actors              import Location, SingleEndPath
from utils.relator              import NameFinder
from readin.stand_in            import StandIn
from readin.description_helpers import Description, PlainTextContext, PlainTextDescription

def add_to_name_space(name_space:NameFinder) -> None:
    north_path = SingleEndPath(
        name="Hallway North Exit",
        description=Description[PlainTextContext](PlainTextContext("To the north, you see a doorway."), PlainTextDescription()),
        end=StandIn[Location]("bedroom", "location")
    )

    south_path = SingleEndPath(
        name="Hallway South Exit",
        description=Description[PlainTextContext](PlainTextContext("Southwards lies a doorway."), PlainTextDescription()),
        end=StandIn[Location]("den", "location")
    )

    east_path = SingleEndPath(
        name="Hallway East Exit",
        description=Description[PlainTextContext](PlainTextContext("To the east is a doorway."), PlainTextDescription()),
        end=StandIn[Location]("kitchen", "location")
    )

    location = Location(
        name="Hallway",
        description=Description[PlainTextContext](PlainTextContext("You are standing in a shadowy hallway. There is a faint smell of mildew."), PlainTextDescription()),
        paths={
            name_space.get_from_id('north', 'direction') : north_path,
            name_space.get_from_id('south', 'direction') : south_path,
            name_space.get_from_id('east',  'direction') : east_path
        }
    )
    name_space.add_many([south_path, north_path, east_path, location])
