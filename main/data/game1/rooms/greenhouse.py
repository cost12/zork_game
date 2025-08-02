from models.actors              import Location, SingleEndPath, LocationDetail
from utils.relator              import NameFinder
from readin.stand_in            import StandIn
from readin.description_helpers import Description, PlainTextContext, PlainTextDescription, ContentsContext, ContentsDescription

def add_to_name_space(name_space:NameFinder) -> None:
    north_path = SingleEndPath(
        name="Greenhouse North Exit",
        description=Description[PlainTextContext](PlainTextContext("A passage leads north."), PlainTextDescription()),
        end=StandIn[Location]("beehive room", "location")
    )

    east_path = SingleEndPath(
        name="Greenhouse East Exit",
        description=Description[PlainTextContext](PlainTextContext("A passage leads east."), PlainTextDescription()),
        end=StandIn[Location]("crystal cave", "location")
    )

    child = LocationDetail(
        name="wall",
        description=Description[ContentsContext](ContentsContext("Hanging from a peg in the wall is", None), ContentsDescription()),
        children=[name_space.get_from_id("dried herbs", "target")]
    )

    location = Location(
        name="Greenhouse",
        description=Description[PlainTextContext](PlainTextContext("You stand in the middle of a large, deserted greenhouse. Any plants that grew here are long dead."), PlainTextDescription()),
        paths={
            name_space.get_from_id('north', 'direction') : north_path,
            name_space.get_from_id('east',  'direction') : east_path
        },
        children=[child]
    )
    name_space.add_many([child, east_path, north_path, location])
