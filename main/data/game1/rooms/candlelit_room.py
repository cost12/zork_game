from models.actors              import Location, LocationDetail, LocationInfo
from utils.relator              import NameFinder
from readin.description_helpers import PlainTextContext, PlainTextDescription, ContentsContext, ContentsDescription

def add_to_name_space(name_space:NameFinder) -> None:
    child = LocationDetail(
        name="floor",
        description_context=ContentsContext("While most of the candles are melted past the point of retrieval, more intact are some candles. Among the handleable candles you see", "All candles on the floor are too melted or misshapen to take."),
		description_strategy=ContentsDescription(),
    )

    location = Location(
        name="Candlelit Room",
        description_context=PlainTextContext("You stand in an elegant room constructed of short terraced marble steps, all of which are covered with lit candles. Their glow illuminates the arched room elegantly."),
		description_strategy=PlainTextDescription(),
        location_info=LocationInfo(),
    )
    name_space.add_many([child, location])
