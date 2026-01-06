from models.actors              import Location, LocationDetail, LocationInfo
from utils.relator              import NameFinder
from readin.description_helpers import PlainTextContext, PlainTextDescription, ContentsContext, ContentsDescription

def add_to_name_space(name_space:NameFinder) -> None:
    child = LocationDetail(
        name="seated",
        description_context=ContentsContext("Sitting idly on a chair is", "All of the seats lie empty"),
		description_strategy=ContentsDescription(),
        #children=[name_space.get_from_id("child", "actor")] TODO
    )

    location = Location(
        name="Coach Car",
        description_context=PlainTextContext("You are standing in a dark, musty shipping container. Its contents are long gone, and only a few piles of rust remain. You hear a shrill sliding melody playing through some hidden speakers."),
		description_strategy=PlainTextDescription(),
        location_info=LocationInfo(),
        #children=[child] TODO
    )

    name_space.add_many([child, location])
