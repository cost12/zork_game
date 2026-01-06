from models.actors              import Location, LocationDetail, LocationInfo
from utils.relator              import NameFinder
#from readin.stand_in            import StandIn
from readin.description_helpers import PlainTextContext, PlainTextDescription, ContentsContext, ContentsDescription

def add_to_name_space(name_space:NameFinder) -> None:
    child = LocationDetail(
        name="table",
        description_context=ContentsContext("On a spindly table you find", "There is a spindly table in the middle of the room."),
        description_strategy=ContentsDescription(),
        #children=[StandIn("leaflet", "target"), StandIn("hourglass", "target"), StandIn("yellow book", "target"), StandIn("lantern", "target")] TODO
    )

    location = Location(
        name="Attic",
        description_strategy=PlainTextContext("You are in a musty, small attic. It is mostly empty, except for a table. At one end of the room is a sooty brick fireplace, leading upwards to the chimney"),
        description_context=PlainTextDescription(),
        location_info=LocationInfo(),
        #children=[child] TODO
    )

    name_space.add_many([child, location])
