from utils.relator import NameFinder
from models.actors import Target
from models.response import StaticResponse
from readin.description_helpers import Description, PlainTextDescription, PlainTextContext
from readin.utils import sdg_from_parts

def add_to_name_space(name_space:NameFinder) -> None:
    sdg = sdg_from_parts(
        unbreakable_states=[name_space.get_from_id("visible",   "state")],
        state_graphs      =[name_space.get_from_id("flammable", "stategraph"),
                            name_space.get_from_id("takeable",  "stategraph")],
        breakable_states  =[name_space.get_from_id("readable",  "state")],
        name_space        =name_space
    )

    note = Target(
        name="note",
        description=Description[PlainTextContext](PlainTextContext("a small handwritten note, scrawled in dark black ink"), PlainTextDescription()),
        states=sdg,
        weight=1,
        value=1,
        size=1,
        target_responses={
            name_space.get_from_id("read",  "action") : StaticResponse("It says: 'May the single instrument transport. When we arrive, let us go on with it in our hearts, if not on our personage.'")
        },
        state_responses={
            name_space.get_from_id("held",   "state") : StaticResponse("You take the note."),
            name_space.get_from_id("broken", "state") : StaticResponse("You rip the note in two, and then four, then eight. Its shreds fall to the floor."),
        }
    )

    name_space.add(note)
