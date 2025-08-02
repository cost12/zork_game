from models.actors              import Location, SingleEndPath, LocationDetail
from utils.relator              import NameFinder
from readin.stand_in            import StandIn
from readin.description_helpers import Description, PlainTextContext, PlainTextDescription, ContentsContext, ContentsDescription

def add_to_name_space(name_space:NameFinder) -> None:
    north_path = SingleEndPath(
        name="Den North Exit",
        description=Description[PlainTextContext](PlainTextContext("To the north is a doorway."), PlainTextDescription()),
        end=StandIn[Location]("hallway", "location")
    )

    south_path = SingleEndPath(
        name="Den South Exit",
        description=Description[PlainTextContext](PlainTextContext("A passageway leads south."), PlainTextDescription()),
        end=StandIn[Location]("garden", "location")
    )

    east_path = SingleEndPath(
        name="Den East Exit",
        description=Description[PlainTextContext](PlainTextContext("A doorway leads east."), PlainTextDescription()),
        end=StandIn[Location]("kitchen", "location")
    )

    west_path = SingleEndPath(
        name="Den West Exit",
        description=Description[PlainTextContext](PlainTextContext("A closed swinging door lies to the west."), PlainTextDescription()),
        end=StandIn[Location]("dining room", "location")
    )

    child = LocationDetail(
        name="couch",
        description=Description[ContentsContext](ContentsContext("Sitting on a troden couch there is", "A trodden couch sits in the middle of the room."), ContentsDescription()),
        children=[name_space.get_from_id("red book", "target"), name_space.get_from_id("wool hat", "target")]
    )

    location = Location(
        name="Den",
        description=Description[PlainTextContext](PlainTextContext("You are standing in a cozy room lit by an overhead lamp with a soft red shade. A once-plump couch sits on a rug in the center of the room, leaking stuffage. "), PlainTextDescription()),
        paths={
            name_space.get_from_id('north', 'direction') : north_path,
            name_space.get_from_id('south', 'direction') : south_path,
            name_space.get_from_id('east',  'direction') : east_path,
            name_space.get_from_id('west',  'direction') : west_path
        },
        children=[child],
    )

    name_space.add_many([north_path, south_path, east_path, child, location])
