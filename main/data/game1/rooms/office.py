from models.actors              import Location, LocationDetail, LocationInfo
from utils.relator              import NameFinder
from readin.description_helpers import PlainTextContext, PlainTextDescription, ContentsContext, ContentsDescription

def add_to_name_space(name_space:NameFinder) -> None:
    child = LocationDetail(
        name="desk",
        description_context=ContentsContext("Sitting on the desk is", "The desk is lacking any contents."),
		description_strategy=ContentsDescription(),
        #children=[name_space.get_from_id("emerald book", "target"), name_space.get_from_id("magnifying glass", "target")] TODO
    )

    location = Location(
        name="Office",
        description_context=PlainTextContext("You are in a simple home office. At a desk sits a large, heavy desktop computer open to a console, its light eerily illuminating the room with a blue glow. There is a spindly chair at the desk."),
		description_strategy=PlainTextDescription(),
        location_info=LocationInfo(),
        #children=[child] TODO
    )

    name_space.add_many([child, location])
