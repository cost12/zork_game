from models.actors              import Location, SingleEndPath, LocationDetail
from utils.relator              import NameFinder
from readin.stand_in            import StandIn
from readin.description_helpers import Description, PlainTextContext, PlainTextDescription, ContentsContext, ContentsDescription

def add_to_name_space(name_space:NameFinder) -> None:
    north_path = SingleEndPath(
        name="Dining Car North Exit",
        description=Description[PlainTextContext](PlainTextContext("You are standing in a train's dining car. A thin counter and spaced stools line the East wall, though no places are set. The train rocks gently, riding Northwards, trees whizzing past as you pass through a dense deciduous forest. A tinkling bouquet of music frolics around the car."), PlainTextDescription()),
        end=StandIn[Location]("Observation Room", "location")
    )

    south_path = SingleEndPath(
        name="Dining Car South Exit",
        description=Description[PlainTextContext](PlainTextContext("The train continues south."), PlainTextDescription()),
        end=StandIn[Location]("coach car", "location")
    )

    child = LocationDetail(
        name="counter",
        description=Description[ContentsContext](ContentsContext("On the counter is", "The counter is empty. Sound familiar?"), ContentsDescription()),
        children=[name_space.get_from_id("gray book", "actor")]
    )

    location = Location(
        name="Dining Car",
        description=Description[PlainTextContext](PlainTextContext("You are in the conductor's car. A complex control panel is next to an exit at the North of the car. An elegant violin concerto plays through the room's speakers."), PlainTextDescription()),
        paths={
            name_space.get_from_id('north', 'direction') : north_path,
            name_space.get_from_id('south', 'direction') : south_path
        },
        children=[child]
    )

    name_space.add_many([north_path, south_path, child, location])
