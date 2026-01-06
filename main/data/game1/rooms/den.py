from models.actors              import Location, LocationDetail, LocationInfo
from utils.relator              import NameFinder
from readin.description_helpers import PlainTextContext, PlainTextDescription, ContentsContext, ContentsDescription

def add_to_name_space(name_space:NameFinder) -> None:
    child = LocationDetail(
        name="couch",
        description_context=ContentsContext("Sitting on a troden couch there is", "A trodden couch sits in the middle of the room."),
		description_strategy=ContentsDescription(),
        #children=[name_space.get_from_id("red book", "target"), name_space.get_from_id("wool hat", "target")] TODO
    )

    location = Location(
        name="Den",
        description_context=PlainTextContext("You are standing in a cozy room lit by an overhead lamp with a soft red shade. A once-plump couch sits on a rug in the center of the room, leaking stuffage. "),
		description_strategy=PlainTextDescription(),
        location_info=LocationInfo(),
        #children=[child], TODO
    )

    name_space.add_many([child, location])
