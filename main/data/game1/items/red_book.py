from utils.relator import NameFinder
from models.actors import Target, TargetInfo
from readin.description_helpers import PlainTextDescription, PlainTextContext, plain_text_description
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
        name="red book",
        aliases=["book"],
        description_context=PlainTextContext("a little book with a red cover"),
        description_strategy=PlainTextDescription(),
        weight=1,
        value=1,
        size=1,
        target_info=TargetInfo(
            states=sdg,
            target_responses={
                name_space.get_from_id("read",  "action") : plain_text_description("You try to read the book, but its script is one which you can neither recognize nor decipher.")
            },
            state_responses={
                name_space.get_from_id("held",   "state") : plain_text_description("You take the Red Book."),
                name_space.get_from_id("broken", "state") : plain_text_description("You rip the book in two, destroying its readability. Nice going...")
            }
        )
    )

    name_space.add(book)
