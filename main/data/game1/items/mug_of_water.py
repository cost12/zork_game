from utils.relator              import NameFinder
from models.actors              import Target, LocationDetail, ItemLimit, TargetInfo
from readin.description_helpers import Description, ContentsContext, ContentsDescription, plain_text_description, ContentsWithStateContext, ContentsWithStateDescription
from readin.utils               import sdg_from_parts
from readin.stand_in            import StandIn

def add_to_name_space(name_space:NameFinder) -> None:
    sdg = sdg_from_parts(
        unbreakable_states=[name_space.get_from_id("visible",   "state")],
        state_graphs      =[name_space.get_from_id("container sg", "stategraph"),
                            name_space.get_from_id("takeable sg", "stategraph")],
        name_space        =name_space
    )

    inside = LocationDetail(
        name="in",
        name_id="in mug",
        item_limit=ItemLimit(1, 1),
        #children=[StandIn("water", "target")] TODO
    )

    mug = Target(
        name="mug",
        description_context=ContentsContext("a small ceramic mug full of", "an empty ceramic mug"),
        description_strategy=ContentsDescription(),
        #children=[inside], TODO
        weight=1,
        value=1,
        size=1,
        target_info=TargetInfo(
            states=sdg,
            target_responses={
                name_space.get_from_id("pour",  "action") : Description[ContentsWithStateContext](StandIn("mug", "target"), ContentsWithStateContext({name_space.get_from_id("liquid", "state") : "You empty the mug's contents, making a bit of a mess..."}, default="You turn the mug upside down, but nothing comes out."), ContentsWithStateDescription()),
            },
            state_responses={
                name_space.get_from_id("held",   "state") : Description[ContentsWithStateDescription](StandIn("mug", "target"), ContentsWithStateContext({name_space.get_from_id("liquid", "state") : "You take the mug. Be fareful not to slosh!"}, default="You take the mug."), ContentsWithStateDescription()),
                name_space.get_from_id("broken", "state") : plain_text_description("The mug is broken and can't be put back together again. Pity..."),
            },
        ),
        item_responses={
            StandIn("honey",   "target") : plain_text_description("The mug is full of honey."),
            StandIn("water",   "target") : plain_text_description("The mug is full of water."),
            StandIn("peppers", "target") : plain_text_description("The mug is full of peppers. Ew.")
        }
    )

    name_space.add_many([mug, inside])
