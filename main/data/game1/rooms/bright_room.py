from models.actors              import Location, LocationInfo
from readin.description_helpers import PlainTextContext, PlainTextDescription
from readin.restriction_helpers import Restriction, CharacterWearingRestriciton, CharacterWearingContext
from utils.relator              import NameFinder

def add_to_name_space(name_space:NameFinder) -> None:
    bright_room = Location(
        name="Bright Room",
        description_context=PlainTextContext("The room is possessed by an overwhelmingly bright light. By squinting hard, you can just barely make out an eerily smooth room."),
		description_strategy=PlainTextDescription(),
        location_info=LocationInfo(
            action_restrictions = {
                name_space.get_from_id("look", 'action') : [Restriction[CharacterWearingContext](CharacterWearingContext(name_space.get_from_id("Sunglasses", "location"), "[Bright Room]\nUpon entering the room, a shockingly bright light strikes your eyes, forcing you to shut them tight. You simply cannot bear to open them."), CharacterWearingRestriciton())]
            }
        ),
    )

    name_space.add_many([bright_room])
