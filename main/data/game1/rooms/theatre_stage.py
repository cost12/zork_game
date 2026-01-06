from models.actors              import Location, LocationDetail, LocationInfo
from utils.relator              import NameFinder
from readin.description_helpers import PlainTextContext, PlainTextDescription, ContentsContext, ContentsDescription

def add_to_name_space(name_space:NameFinder) -> None:
    child1 = LocationDetail(
        name="stage",
        description_context=ContentsContext("Laying abandoned on the stage is", "The stage is empty and barren."),
		description_strategy=ContentsDescription(),
        #children= [name_space.get_from_id("lyre",          "target"), name_space.get_from_id("triangle",      "target"), name_space.get_from_id("slide whistle", "target"), name_space.get_from_id("bongo",         "target"), name_space.get_from_id("violin",        "target")] TODO
    )

    child2 = LocationDetail(
        name="stand",
        description_context=ContentsContext("Sitting on the music stand is", None),
		description_strategy=ContentsDescription(),
        #children=[name_space.get_from_id("baton", "target"), name_space.get_from_id("note",  "target")] TODO
    )

    location = Location(
        name="Theatre Stage",
        description_context=PlainTextContext("You stand on a meekly lit Theatre Stage. A lone music stand stands proudly on the stage."),
		description_strategy=PlainTextDescription(),
        location_info=LocationInfo(),
        #children=[child1, child2] TODO
    )

    name_space.add_many([child2, child1, location])
