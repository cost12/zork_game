from utils.relator              import NameFinder
from models.named               import NameInfo
from models.actors              import Actor, ItemLimit, TargetInfo, ActorInfo, ContainerInfo, VisibleInfo
from readin.description_helpers import plain_text_description
from readin.utils               import sdg_from_parts, get_inventory

def add_to_name_space(name_space:NameFinder) -> None:
    sdg = sdg_from_parts(
        name_space=name_space,
        state_graphs=[name_space.get_from_id("standard_character")]
    )

    inventory = get_inventory(bear, ItemLimit(200, 100))

    bear = Actor(
        name_info=NameInfo(
            name="Bear",
            description_context="",
            description_strategy="",
            aliases=[]
        ),
        target_info=TargetInfo(

        ),
        actor_info=ActorInfo(

        ),
        container_info=ContainerInfo(

        ),
        visible_info=VisibleInfo(
            
        )
    )
    
    
    (
        
        type="bear",
        description=(plain_text, "a bear."),
        states=sdg,
        skills=name_space.get_from_id("standard"),
        children=[inventory],
        target_responses={
            name_space.get_from_id("look",   "action") : StaticResponse("You see a bear"),
            name_space.get_from_id("take",   "action") : StaticResponse("A foolish endeavor."),
            name_space.get_from_id("attack", "action") : StaticResponse("With what?"),
            name_space.get_from_id("hug",    "action") : StaticResponse("This merely confuses and angers the Bear"),
            name_space.get_from_id("kiss",   "action") : StaticResponse("The Bear thinks you are cute and kisses you back. With gusto!")
        }
    )

    name_space.add_many([bear,inventory])
