from models.actors              import Location, SingleEndPath, LocationDetail
from utils.relator              import NameFinder
from readin.stand_in            import StandIn
from readin.description_helpers import Description, PlainTextContext, PlainTextDescription, ContentsContext, ContentsDescription

def add_to_name_space(name_space:NameFinder) -> None:
    north_path = SingleEndPath(
        name="Conductor's Car North Exit",
        description=Description[PlainTextContext](PlainTextContext("The train's exit is to the North."), PlainTextDescription()),
        end=StandIn[Location]("Hot Room", "location")
    )

    south_path = SingleEndPath(
        name="Conductor's Car South Exit",
        description=Description[PlainTextContext](PlainTextContext("The train continues southwards."), PlainTextDescription()),
        end=StandIn[Location]("cargo hold", "location")
    )

    child = LocationDetail(
        name="dashboard",
        description=Description[ContentsContext](ContentsContext("On the dashboard, amidst an array of rusty knobs and buttons lies", "The slew of controls and buttons lies neglected and empty"), ContentsDescription()),
        children=[name_space.get_from_id("burgundy book", "actor")]
    )

    location = Location(
        name="Conductor's Car",
        description=Description[PlainTextContext](PlainTextContext("You are in the conductor's car. A complex control panel is next to an exit at the North of the car. An elegant violin concerto plays through the room's speakers."), PlainTextDescription()),
        paths={
            name_space.get_from_id('north', 'direction') : north_path,
            name_space.get_from_id('south', 'direction') : south_path
        },
        children=[child]
    )
    name_space.add_many([north_path, south_path, child, location])
