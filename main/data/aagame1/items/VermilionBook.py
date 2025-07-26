from utils.relator import NameFinder
from models.actors import Target
from models.response import StaticResponse
from readin.description_helpers import plain_text
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
        name="vermilion book",
        aliases=["book"],
        description=Description[PlainTextContext](PlainTextContext("a lovely book with a distinctly vermilion cover"), PlainTextDescription()),
        states=sdg,
        weight=1,
        value=1,
        size=1,
        target_responses={
            name_space.get_from_id("read", "action") : StaticResponse("You try to read the book, but its script is one which you can neither recognize nor decipher.")
        },
        state_responses={
            name_space.get_from_id("held",   "state") : StaticResponse("You take the Vermilion Book."),
            name_space.get_from_id("broken", "state") : StaticResponse("You rip the book in two, destroying its readability. Nice going...")
        }
    )

    name_space.add(book)
