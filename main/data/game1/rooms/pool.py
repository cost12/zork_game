from models.actors              import Location, SingleEndPath
from utils.relator              import NameFinder
from readin.stand_in            import StandIn
from readin.description_helpers import Description, PlainTextContext, PlainTextDescription

def add_to_name_space(name_space:NameFinder) -> None:
    north_path = SingleEndPath(
        name="Pool North Exit",
        description=Description[PlainTextContext](PlainTextContext("A cool passage leads north, emitting a cool breeze."), PlainTextDescription()),
        end=StandIn[Location]("crystal cave", "location")
    )

    south_path = SingleEndPath(
        name="Pool South Exit",
        description=Description[PlainTextContext](PlainTextContext("A passage leads south, smelling of body odor."), PlainTextDescription()),
        end=StandIn[Location]("gym", "location")
    )

    location = Location(
        name="Pool",
        description=Description[PlainTextContext](PlainTextContext("You stand at the edge of a large pool lying between you and the opposite exit, stretching from wall to wall. Small waves lap at the pool's edge. It looks deep, and the room is cold. Carrying too much weight while swimming across seems unwise."), PlainTextDescription()),
        paths={
            name_space.get_from_id('north', 'direction') : north_path,
            name_space.get_from_id('south', 'direction') : south_path
        }
    )
    name_space.add_many([south_path, north_path, location])
