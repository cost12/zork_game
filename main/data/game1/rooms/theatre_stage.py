from models.actors              import Location, LocationDetail, LocationInfo
from utils.relator              import NameFinder
from readin.description_helpers import PlainTextContext, PlainTextDescription, ContentsContext, ContentsDescription

def add_to_name_space(name_space:NameFinder) -> None:
    child1 = LocationDetail(
        name="stage",
        description_context=ContentsContext("Laying abandoned on the stage is", "The stage is empty and barren."),
		description_strategy=ContentsDescription(),
    )

    child2 = LocationDetail(
        name="stand",
        description_context=ContentsContext("Sitting on the music stand is", None),
		description_strategy=ContentsDescription(),
    )

    location = Location(
        name="Theatre Stage",
        description_context=PlainTextContext("You stand on a meekly lit Theatre Stage. A lone music stand stands proudly on the stage."),
		description_strategy=PlainTextDescription(),
        location_info=LocationInfo(),
    )

    name_space.add_many([child2, child1, location])
