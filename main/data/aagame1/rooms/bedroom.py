from models.actors import Actor, Target, Location, LocationDetail, SingleEndPath
from models.requirement import ItemStateRequirement
from models.named import Action, Direction
from models.state import State
from utils.relator import NameFinder
from readin.stand_in import StandIn
from readin.description_helpers import plain_text, contents_text
    
east_path = SingleEndPath(
    name="Bedroom East Exit",
    description="To the east, you see a doorway.",
    end=StandIn[Location]("Bathroom", "location")
)

def up_path_description(action:Action, success:bool, character:Actor, target:Target, tool:Target, trapdoor:Target) -> str:
    return f"Above your head is {trapdoor.get_description_to(character)} in the ceiling."

up_path = SingleEndPath(
    name="Bedroom Up Exit",
    description=(up_path_description, StandIn[Target]("trapdoor", "target")),
    end=StandIn[Location]("Attic", "location"),
    children=[StandIn[Target]("trapdoor", "target")],
    passing_requirements=ItemStateRequirement({
        StandIn[Target]("trapdoor", "target") : {
            StandIn[State]("open", "state") : [True, None]
        }
    })
)

south_path = SingleEndPath(
    name="Bedroom South Exit",
    description=(plain_text, "A passage stretches south."),
    end=StandIn[Location]("Hallway", "location")
)

bedside = LocationDetail(
    name="Bedside",
    description=(contents_text, (StandIn[Location]("Bedside", "locationdetail"), "Next to the bed sits an empty table.", "On the bedside table rests")),
    children=[StandIn("mug", "target"), StandIn("brown book", "target")]
)

bedroom = Location(
    name="Bedroom",
    description=(plain_text, "You are in a humble bedroom. A small bed lines one wall. It looks cozy. Feeble light seeps through a small overhead light."),
    paths={
        StandIn[Direction]("east",  "direction")  : east_path,
        StandIn[Direction]("up",    "direction")  : up_path,
        StandIn[Direction]("south", "direction")  : south_path
    },
    children=[bedside, StandIn[Actor]("player1", "actor")],
    start_location=True
)

def add_to_name_space(name_space:NameFinder) -> None:
    name_space.add_many([east_path, up_path, south_path, bedside, bedroom])
