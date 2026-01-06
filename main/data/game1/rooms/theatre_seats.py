from models.actors              import Location, LocationDetail, LocationInfo
from utils.relator              import NameFinder
from readin.description_helpers import PlainTextContext, PlainTextDescription, ContentsContext, ContentsDescription

def add_to_name_space(name_space:NameFinder) -> None:
    child = LocationDetail(
        name="in seat",
        description_context=ContentsContext("Sewn inside of the seat", None),
		description_strategy=ContentsDescription(),
        #children=[name_space.get_from_id("keys", "target")], TODO
        hidden=True
    )

    location = Location(
        name="Theatre Seats",
        description_context=PlainTextContext("You stand in the aisle between two large sections of seats. To the East are seats 1-10, to the west are seats 11-20. Each row is labeled with a letter, from A at the South to row J at the North."),
		description_strategy=PlainTextDescription(),
        location_info=LocationInfo(),
        #children=[child] TODO
    )

    name_space.add_many([child, location])
