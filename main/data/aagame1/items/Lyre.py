from utils.relator              import NameFinder
from models.actors              import Target
from models.response            import StaticResponse
from readin.description_helpers import plain_text
from readin.utils               import sdg_from_parts

def add_to_name_space(name_space:NameFinder) -> None:
    sdg = sdg_from_parts(
        unbreakable_states=[name_space.get_from_id("visible",  "state")],
        state_graphs      =[name_space.get_from_id("takeable", "stategraph")],
        breakable_states  =[name_space.get_from_id("musical",  "state")],
        name_space        =name_space
    )

    lyre = Target(
        name="lyre",
        description=(plain_text, "a rustic Greek lyre, surely loved as is evident from the well-worn neck"),
        states=sdg,
        weight=2,
        value=10,
        size=1,
        target_responses={
            name_space.get_from_id("play",  "action") : StaticResponse("You're not very good, but the spirit seems to stay your novice hand, and you are able to stumble through a simple yet haunting melody.")
        },
        state_responses={
            name_space.get_from_id("held",   "state") : StaticResponse("You momentarily feel transported back to Ancient Athênai as a the spirit of a minstrel fleetingly posesses you."),
            name_space.get_from_id("broken", "state") : StaticResponse("Why oh why? The olden lyre so lovingly passed down between generations is no more.")
        }
    )

    name_space.add(lyre)
