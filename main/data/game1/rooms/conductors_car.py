from models.actors              import Location, LocationDetail, LocationInfo
from utils.relator              import NameFinder
from readin.description_helpers import PlainTextContext, PlainTextDescription, ContentsContext, ContentsDescription

def add_to_name_space(name_space:NameFinder) -> None:
    child = LocationDetail(
        name="dashboard",
        description_context=ContentsContext("On the dashboard, amidst an array of rusty knobs and buttons lies", "The slew of controls and buttons lies neglected and empty"),
		description_strategy=ContentsDescription(),
        #children=[name_space.get_from_id("burgundy book", "actor")] TODO
    )

    location = Location(
        name="Conductor's Car",
        description_context=PlainTextContext("You are in the conductor's car. A complex control panel is next to an exit at the North of the car. An elegant violin concerto plays through the room's speakers."),
		description_strategy=PlainTextDescription(),
        location_info=LocationInfo(),
        #children=[child] TODO
    )

    name_space.add_many([child, location])
