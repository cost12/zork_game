from models.actors              import Location, SingleEndPath, LocationDetail
from utils.relator              import NameFinder
from readin.stand_in            import StandIn
from readin.description_helpers import Description, PlainTextContext, PlainTextDescription, ContentsContext, ContentsDescription

def add_to_name_space(name_space:NameFinder) -> None:
    north_path = SingleEndPath(
        name="Theatre Seats North Exit",
        description=Description[PlainTextContext](PlainTextContext("The Theatre's entryway lies in the north."), PlainTextDescription()),
        end=StandIn[Location]("Theatre Entrance", "location")
    )

    south_path = SingleEndPath(
        name="Theatre Seats South Exit",
        description=Description[PlainTextContext](PlainTextContext("The Theatre's stage is southwards."), PlainTextDescription()),
        end=StandIn[Location]("Theatre Stage", "location")
    )

    child = LocationDetail(
        name="in seat",
        description=Description[ContentsContext](ContentsContext("Sewn inside of the seat", None), ContentsDescription()),
        children=[name_space.get_from_id("keys", "target")],
        hidden=True
    )

    location = Location(
        name="Theatre Seats",
        description=Description[PlainTextContext](PlainTextContext("You stand in the aisle between two large sections of seats. To the East are seats 1-10, to the west are seats 11-20. Each row is labeled with a letter, from A at the South to row J at the North."), PlainTextDescription()),
        paths={
            name_space.get_from_id('north', 'direction') : north_path,
            name_space.get_from_id('south', 'direction') : south_path
        },
        children=[child]
    )
    name_space.add_many([child, south_path, north_path, location])
