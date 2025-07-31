from models.actors              import Location, MultiEndPath
from utils.relator              import NameFinder
from readin.stand_in            import StandIn
from readin.description_helpers import Description, PlainTextContext, PlainTextDescription

def add_to_name_space(name_space:NameFinder) -> None:
    any_path = MultiEndPath(
        name="Chimney Exit",
        description=Description[PlainTextContext](PlainTextContext("The fireplace opening is at your feet."), PlainTextDescription()),
        end=StandIn[Location]("attic", "location"),
        multi_end={
            name_space.get_from_id("slide whistle", "target") : StandIn("theatre stage", "location")
        }
    )

    location = Location(
        name="Chimney",
        description=Description[PlainTextContext](PlainTextContext("You are standing in a cramped dark space. It smells of smoke. You are quickly covered in soot and ash. Blegh!"), PlainTextDescription()),
        paths={
            name_space.get_from_id('any', 'direction') : any_path
        }
    )
    name_space.add_many([any_path, location])
