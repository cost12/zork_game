from utils.relator              import NameFinder
from models.actors              import Target
from models.response            import StaticResponse
from readin.description_helpers import plain_text
from readin.utils               import sdg_from_parts

def add_to_name_space(name_space:NameFinder) -> None:
    sdg = sdg_from_parts(
        unbreakable_states=[name_space.get_from_id("visible",  "state"),
                            name_space.get_from_id("musical",  "state")],
        state_graphs      =[name_space.get_from_id("takeable", "stategraph")],
        name_space        =name_space
    )

    violin = Target(
        name="violin",
        description=Description[PlainTextContext](PlainTextContext("an elegant violin, seemingly out of place, as if from a bygone era (its caretakers (for surely there have been many generations, between which this delicate masterpiece has been passed) have done well to guard their custody)"), PlainTextDescription()),
        states=sdg,
        weight=2,
        value=10,
        size=1,
        target_responses={
            name_space.get_from_id("play",  "action") : StaticResponse("You're not very good, but the spirit seems to stay your novice hand, and you are able to stumble through a simple yet haunting melody."),
            name_space.get_from_id("break", "action") : StaticResponse("The triangle is a slippery little bugger and you fuund yourself unable to destroy it.")
        },
        state_responses={
            name_space.get_from_id("held",   "state") : StaticResponse("As you reach for the violin, a foreboding gravitas domineers you, and you gain a peripheral grasp on the depth of the instrument's storied past."),
            name_space.get_from_id("broken", "state") : StaticResponse("You devil! The Violin shatters and with it die the dreams of all those who love music, light, and joy in this god-forsaken reaml.")
        }
    )

    name_space.add(violin)
