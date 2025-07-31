from models.actors              import Location, SingleEndPath, LocationDetail
from utils.relator              import NameFinder
from readin.stand_in            import StandIn
from readin.description_helpers import Description, PlainTextContext, PlainTextDescription, ContentsContext, ContentsDescription

def add_to_name_space(name_space:NameFinder) -> None:
    west_path = SingleEndPath(
        name="Display Room West Exit",
        description=Description[PlainTextContext](PlainTextContext("A simple slanted passage leads west."), PlainTextDescription()),
        end=StandIn[Location]("man cave", "location")
    )

    child = LocationDetail(
        name="cushion",
        description=Description[ContentsContext](ContentsContext("On a velvet cushion rests", "A velvet cushion sits on a pedestal, notably missing the precious item it seems to be meant to hold."), ContentsDescription()),
        children=[name_space.get_from_id("wallet", "target")]
    )

    location = Location(
        name="Display Room",
        description=Description[PlainTextContext](PlainTextContext("You enter a small, dark room with a luxurious velvet carpet."), PlainTextDescription()),
        paths={
            name_space.get_from_id('west',  'direction') : west_path
        },
        children=[child],
    )

    name_space.add_many([child, location, west_path])
a={
    "name"       : "Driver's Seat",
    "description": "You sit in the driver's seat of the car, feeling the cool leather on your bottom.",
    "paths"      : {
        "out"    : {
            "name"        : "Exit 1",
            "description" : "The door leads out",
            "end"         : "Parking Lot"
        }
    },
    "details"    : [
        {
            "name"        : "mirror",
            "description" : {
                "type"    : "contents",
                "full"    : "Hanging from the neck of the rearview mirror is",
                "empty"   : "The rearview mirror is undecorated, and with it you can see into the empty lot"
            },"contents"    : ["Sunglasses"]
        }
    ]
}