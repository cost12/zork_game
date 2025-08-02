from utils.relator import NameFinder
from models.actors import Target
from models.response import StaticResponse
from readin.description_helpers import Description, PlainTextDescription, PlainTextContext
from readin.utils import sdg_from_parts

def add_to_name_space(name_space:NameFinder) -> None:
    sdg = sdg_from_parts(
        unbreakable_states=[name_space.get_from_id("visible",   "state")],
        state_graphs      =[name_space.get_from_id("takeable",  "stategraph"),
                            name_space.get_from_id("flammable", "stategraph")],
        breakable_states  =[name_space.get_from_id("readable",  "state")],
        name_space        =name_space
    )

    book = Target(
        name="yellow book",
        aliases=["book", "paperback", "book with slip", "paperback with a garish yellow slip"],
        description=Description[PlainTextContext](PlainTextContext("a nice paperback with a garish yellow slip"), PlainTextDescription()),
        states=sdg,
        weight=1,
        value=1,
        size=1,
        target_responses={
            name_space.get_from_id("read", "action") : StaticResponse("You try to read the book, but its script is one which you can neither recognize nor decipher.")
        },
        state_responses={
            name_space.get_from_id("held",   "state") : StaticResponse("You take the Yellow Book."),
            name_space.get_from_id("broken", "state") : StaticResponse("You rip the book in two, destroying its readability. Nice going...")
        }
    )

    name_space.add(book)
