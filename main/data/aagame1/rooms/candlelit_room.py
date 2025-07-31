from models.actors              import Location, SingleEndPath, LocationDetail
from utils.relator              import NameFinder
from readin.stand_in            import StandIn
from readin.description_helpers import Description, PlainTextContext, PlainTextDescription, ContentsContext, ContentsDescription

def add_to_name_space(name_space:NameFinder) -> None:
    east_path = SingleEndPath(
        name="Candlelit Room East Exit",
        description=Description[PlainTextContext](PlainTextContext("A thin passage slithers eastward."), PlainTextDescription()),
        end=StandIn[Location]("Giant Cave", "location")
    )

    south_path = SingleEndPath(
        name="Candlelit Room South Exit",
        description=Description[PlainTextContext](PlainTextContext("A grand, ornate doorway leads south, bejewled and intricately chiseled with themes of old."), PlainTextDescription()),
        end=StandIn[Location]("Riches Room", "location")
    )

    child = LocationDetail(
        name="floor",
        description=Description[ContentsContext](ContentsContext("While most of the candles are melted past the point of retrieval, more intact are some candles. Among the handleable candles you see", "All candles on the floor are too melted or misshapen to take."), ContentsDescription()),
        children=[
            StandIn("beeswax candle", "target"),
            StandIn("small candle", "target"),
            StandIn("square candle", "target"),
            StandIn("thin candle", "target"),
            StandIn("squat candle", "target")
        ]
    )

    location = Location(
        name="Candlelit Room",
        description=Description[PlainTextContext](PlainTextContext("You stand in an elegant room constructed of short terraced marble steps, all of which are covered with lit candles. Their glow illuminates the arched room elegantly."), PlainTextDescription()),
        paths={
            name_space.get_from_id('east',  'direction') : east_path,
            name_space.get_from_id('south', 'direction') : south_path
        },
        children=[child],
    )
    name_space.add_many([east_path, south_path, child, location])
