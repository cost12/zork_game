from models.actors              import Location, SingleEndPath
from utils.relator              import NameFinder
from readin.stand_in            import StandIn
from readin.description_helpers import Description, PlainTextContext, PlainTextDescription

def add_to_name_space(name_space:NameFinder) -> None:
    east_path = SingleEndPath(
        name="Cellar East Exit",
        description=Description[PlainTextContext](PlainTextContext("A stone staircase leads east."), PlainTextDescription()),
        end=StandIn[Location]("garden", "location")
    )

    location = Location(
        name="Cellar",
        description=Description[PlainTextContext](PlainTextContext("You enter a damp, dark cellar with stone walls. Water leaks down one wall slowly. In a corner is a large trunk."), PlainTextDescription()),
        paths={
            name_space.get_from_id('east', 'direction') : east_path
        },
        children=[name_space.get_from_id("trunk", "target")]
    )
    name_space.add_many([east_path, location])
