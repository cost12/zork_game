from models.actors              import Location, LocationDetail, LocationInfo
from utils.relator              import NameFinder
from readin.description_helpers import PlainTextContext, PlainTextDescription, ContentsContext, ContentsDescription

def add_to_name_space(name_space:NameFinder) -> None:
    child = LocationDetail(
        name="ground",
        description_context=ContentsContext("On the ground sits", None),
		description_strategy=ContentsDescription(),
    )

    location = Location(
        name="Garden",
        description_context=PlainTextContext("You are standing in a small garden. The planter beds are devoid of life, the soil seems dry. The drab facade of a house in disrepair forms the northern border of the yard, with tall wooden fences on all other sides."),
		description_strategy=PlainTextDescription(),
        location_info=LocationInfo(),
    )

    name_space.add_many([child, location])
