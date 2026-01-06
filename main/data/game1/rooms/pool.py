from models.actors              import Location, LocationInfo
from utils.relator              import NameFinder
from readin.description_helpers import PlainTextContext, PlainTextDescription

def add_to_name_space(name_space:NameFinder) -> None:
    

    location = Location(
        name="Pool",
        description_context=PlainTextContext("You stand at the edge of a large pool lying between you and the opposite exit, stretching from wall to wall. Small waves lap at the pool's edge. It looks deep, and the room is cold. Carrying too much weight while swimming across seems unwise."),
		description_strategy=PlainTextDescription(),
        location_info=LocationInfo(),
    )

    name_space.add_many([location])
