from utils.relator              import NameFinder
from models.actors              import Target
from models.response            import StaticResponse
from readin.description_helpers import Description, PlainTextDescription, PlainTextContext
from readin.utils               import sdg_from_parts

def add_to_name_space(name_space:NameFinder) -> None:
    sdg = sdg_from_parts(
        unbreakable_states=[name_space.get_from_id("visible",   "state")],
        state_graphs      =[name_space.get_from_id("switch",  "stategraph")],
        name_space        =name_space
    )

    shower = Target(
        name="shower",
        description=Description[PlainTextContext](PlainTextContext("a stained shower occupying one wall"), PlainTextDescription()),
        states=sdg,
        weight=100,
        value=5,
        size=50,
        target_responses={
            name_space.get_from_id("take", "action")  : StaticResponse("You can't take the shower, dummy. Besides, it's pretty gross... whoever lives here must be a bit of a slob")
        },
        state_responses={
            name_space.get_from_id("on",     "state") : StaticResponse("The shower's faucet turns, but only a trickle of dust comes out of the showerhead."),
            name_space.get_from_id("off",    "state") : StaticResponse("The faucet turns is off."),
            name_space.get_from_id("broken", "state") : StaticResponse("Now that's just gratuitous!")
        }
    )

    name_space.add(shower)
