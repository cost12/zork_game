from models.actors import Location, SingleEndPath, Actor, Target
from models.named  import Direction
from models.response import Response
from readin.description_helpers import plain_text
from readin.stand_in import StandIn
from utils.relator import NameFinder

northeast_path = SingleEndPath(
    name        = "Bright Room Northeast Exit",
    description = (plain_text, "A passage exists, but you cannot tell in which direction, for you are nearly blinded by the light."),
    end         = StandIn[Location]("Orge Lair", "location")
)

southwest_path = SingleEndPath(
    name        = "Bright Room Southwest Exit",
    description = (plain_text, "Somewhere in your field of vision is a passage, but you are disoriented by the brightness and cannot tell in which direction it lies."),
    end         = StandIn[Location]("Theatre Entrance", "location")
)

def look_restriction(character:Actor, sunglasses:Target) -> tuple[bool, Response]:
    if character.is_wearing(sunglasses):
        return True, None
    return False, "[Bright Room]\nUpon entering the room, a shockingly bright light strikes your eyes, forcing you to shut them tight. You simply cannot bear to open them."

bright_room = Location(
    name        = "Bright Room",
    description = (plain_text, "The room is possessed by an overwhelmingly bright light. By squinting hard, you can just barely make out an eerily smooth room."),
    paths       = {
        StandIn[Direction]("Northeast", "direction"): northeast_path,
        StandIn[Direction]("Southwest", "direction"): southwest_path
    },
    action_restrictions = {
        "look" : (look_restriction, StandIn[Target]("Sunglasses", "location"))
    }
)

def add_to_name_space(name_space:NameFinder) -> None:
    name_space.add_many([northeast_path, southwest_path, bright_room])