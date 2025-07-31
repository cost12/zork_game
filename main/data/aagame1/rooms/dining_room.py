from models.actors              import Location, SingleEndPath, LocationDetail
from utils.relator              import NameFinder
from readin.stand_in            import StandIn
from readin.description_helpers import Description, PlainTextContext, PlainTextDescription, ContentsContext, ContentsDescription

def add_to_name_space(name_space:NameFinder) -> None:
    north_path = SingleEndPath(
        name="Dining Room North Exit",
        description=Description[PlainTextContext](PlainTextContext("A doorway leads north."), PlainTextDescription()),
        end=StandIn[Location]("office", "location")
    )

    east_path = SingleEndPath(
        name="Dining Room East Exit",
        description=Description[PlainTextContext](PlainTextContext("A door goes east."), PlainTextDescription()),
        end=StandIn[Location]("den", "location")
    )

    child = LocationDetail(
        name="table",
        id="table2",
        description=Description[ContentsContext](ContentsContext("On the table sits", "The table is bare and free of burden. That must be nice"), ContentsDescription()),
        children=[name_space.get_from_id("plate", "target")]
    )

    location = Location(
        name="Dining Room",
        description=Description[PlainTextContext](PlainTextContext("You are standing in a rectangular room with a rough-hewn wooden table in the middle."), PlainTextDescription()),
        paths={
            name_space.get_from_id('north', 'direction') : north_path,
            name_space.get_from_id('east',  'direction') : east_path
        },
        children=[child]
    )

    name_space.add_many([north_path, east_path, child, location])
