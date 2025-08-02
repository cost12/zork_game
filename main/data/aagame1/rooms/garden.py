from models.actors              import Location, SingleEndPath, LocationDetail
from utils.relator              import NameFinder
from readin.stand_in            import StandIn
from readin.description_helpers import Description, PlainTextContext, PlainTextDescription, ContentsContext, ContentsDescription

def add_to_name_space(name_space:NameFinder) -> None:
    north_path = SingleEndPath(
        name="Garden North Exit",
        description=Description[PlainTextContext](PlainTextContext("The house's tattered front door lies to the north, slightly ajar."), PlainTextDescription()),
        end=StandIn[Location]("Den", "location")
    )

    south_path = SingleEndPath(
        name="Garden South Exit",
        description=Description[PlainTextContext](PlainTextContext("A narrow earthen burrow leads south."), PlainTextDescription()),
        end=StandIn[Location]("earthen tunnel", "location")
    )

    west_path = SingleEndPath(
        name="Garden West Exit",
        description=Description[PlainTextContext](PlainTextContext("A stone stiarcase descends in the west."), PlainTextDescription()),
        end=StandIn[Location]("cellar", "location")
    )

    child = LocationDetail(
        name="ground",
        description=Description[ContentsContext](ContentsContext("On the ground sits", None), ContentsDescription()),
        children=[name_space.get_from_id("thick gloves", "target"), name_space.get_from_id("trowel", "target")]
    )

    location = Location(
        name="Garden",
        description=Description[PlainTextContext](PlainTextContext("You are standing in a small garden. The planter beds are devoid of life, the soil seems dry. The drab facade of a house in disrepair forms the northern border of the yard, with tall wooden fences on all other sides."), PlainTextDescription()),
        paths={
            name_space.get_from_id('north', 'direction') : north_path,
            name_space.get_from_id('south', 'direction') : south_path,
            name_space.get_from_id('west',  'direction') : west_path
        },
        children=[child]
    )
    name_space.add_many([child, west_path, south_path, north_path, location])
