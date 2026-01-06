from models.actors              import Location, LocationDetail, LocationInfo
from utils.relator              import NameFinder
from readin.description_helpers import PlainTextContext, PlainTextDescription, ContentsContext, ContentsDescription



def add_to_name_space(name_space:NameFinder) -> None:
    bedside = LocationDetail(
        name="Bedside",
        description_context=ContentsContext("On the bedside table rests", "Next to the bed sits an empty table."),
		description_strategy=ContentsDescription(),
        #children=[StandIn("mug", "target"), StandIn("brown book", "target")] TODO
    )

    bedroom = Location(
        name="Bedroom",
        description_context=PlainTextContext("You are in a humble bedroom. A small bed lines one wall. It looks cozy. Feeble light seeps through a small overhead light."),
		description_strategy=PlainTextDescription(),
        #children=[bedside, StandIn[Actor]("player1", "actor")], TODO
        location_info=LocationInfo(
            is_start_location=True
        )
    )

    name_space.add_many([bedside, bedroom])
