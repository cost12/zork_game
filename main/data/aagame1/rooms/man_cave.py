from models.actors              import Location, SingleEndPath
from utils.relator              import NameFinder
from readin.stand_in            import StandIn
from readin.description_helpers import Description, PlainTextContext, PlainTextDescription

def add_to_name_space(name_space:NameFinder) -> None:
    northwest_path = SingleEndPath(
        name="Man Cave Northwest Exit",
        description=Description[PlainTextContext](PlainTextContext("A passage leads northwest."), PlainTextDescription()),
        end=StandIn[Location]("theatre stage", "location")
    )

    south_path = SingleEndPath(
        name="Man Cave South Exit",
        description=Description[PlainTextContext](PlainTextContext("A passage leads south."), PlainTextDescription()),
        end=StandIn[Location]("north of tight pass", "location")
    )

    east_path = SingleEndPath(
        name="Man Cave East Exit",
        description=Description[PlainTextContext](PlainTextContext("An ornate doorway leads to the east."), PlainTextDescription()),
        end=StandIn[Location]("display room", "location")
    )

    location = Location(
        name="Man Cave",
        description=Description[PlainTextContext](PlainTextContext("You enter a well-furnished man cave. Posters of scanty models, brawny wrestlers, and feline predators adorn every inch of wall."), PlainTextDescription()),
        paths={
            name_space.get_from_id('northwest', 'direction') : northwest_path,
            name_space.get_from_id('south',     'direction') : south_path,
            name_space.get_from_id('east',      'direction') : east_path
        },
        children=[name_space.get_from_id("bully", "actor")]
    )
    name_space.add_many([east_path, south_path, northwest_path, location])
