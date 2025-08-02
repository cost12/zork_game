from models.actors              import Location, SingleEndPath, MultiEndPath, LocationDetail
from utils.relator              import NameFinder
from readin.stand_in            import StandIn
from readin.description_helpers import Description, PlainTextContext, PlainTextDescription, ContentsContext, ContentsDescription

def add_to_name_space(name_space:NameFinder) -> None:
    north_path = SingleEndPath(
        name="Theatre Stage North Exit",
        description=Description[PlainTextContext](PlainTextContext("The Theatre continues to the north, full of seats."), PlainTextDescription()),
        end=StandIn[Location]("theatre seats", "location")
    )

    southeast_path = MultiEndPath(
        name="Theatre Stage Southeast Exit",
        description=Description[PlainTextContext](PlainTextContext("A passage embellished with arcane runes leads southeast."), PlainTextDescription()),
        end=None,
        multi_end={
            name_space.get_from_id("baton",         "target") : StandIn("carpeted hall",  "location"),
            name_space.get_from_id("lyre",          "target") : StandIn("museum gallery", "location"),
            name_space.get_from_id("triangle",      "target") : StandIn("parking lot",    "location"),
            name_space.get_from_id("slide whistle", "target") : StandIn("chimney",        "location"),
            name_space.get_from_id("bongo",         "target") : StandIn("gym",            "location"),
            name_space.get_from_id("violin",        "target") : StandIn("library",        "location")
        }
    )

    southwest_path = MultiEndPath(
        name="Theatre Stage Southwest Exit",
        description=Description[PlainTextContext](PlainTextContext("A passage garnished with ancient symbology leads southwest."), PlainTextDescription()),
        end=None,
        multi_end={
            name_space.get_from_id("baton",         "target") : StandIn("hot room",       "location"),
            name_space.get_from_id("lyre",          "target") : StandIn("museum gallery", "location"),
            name_space.get_from_id("triangle",      "target") : StandIn("parking lot",    "location"),
            name_space.get_from_id("slide whistle", "target") : StandIn("chimney",        "location"),
            name_space.get_from_id("bongo",         "target") : StandIn("gym",            "location"),
            name_space.get_from_id("violin",        "target") : StandIn("library",        "location")
        }
    )

    child1 = LocationDetail(
        name="stage",
        description=Description[ContentsContext](ContentsContext("Laying abandoned on the stage is", "The stage is empty and barren."), ContentsDescription()),
        children=[
            name_space.get_from_id("lyre",          "target"),
            name_space.get_from_id("triangle",      "target"),
            name_space.get_from_id("slide whistle", "target"),
            name_space.get_from_id("bongo",         "target"),
            name_space.get_from_id("violin",        "target")
        ]
    )

    child2 = LocationDetail(
        name="stand",
        description=Description[ContentsContext](ContentsContext("Sitting on the music stand is", None), ContentsDescription()),
        children=[
            name_space.get_from_id("baton", "target"),
            name_space.get_from_id("note",  "target")
        ]
    )

    location = Location(
        name="Theatre Stage",
        description=Description[PlainTextContext](PlainTextContext("You stand on a meekly lit Theatre Stage. A lone music stand stands proudly on the stage."), PlainTextDescription()),
        paths={
            name_space.get_from_id('north',     'direction') : north_path,
            name_space.get_from_id('southeast', 'direction') : southeast_path,
            name_space.get_from_id('southwest', 'direction') : southwest_path
        },
        children=[child1, child2]
    )
    name_space.add_many([child2, child1, southwest_path, southeast_path, north_path, location])
