from typing import Callable

from .world import World, WorldRules

def simple_interaction() -> Callable[[str,WorldRules,World,str,str,dict[str,str],Callable[[str],None]],bool]:
    def interaction(own_id: str, rules: WorldRules, world: World, other_id: str, action_id: str, inputs: dict[str,str], inform: Callable[[str],None]) -> bool:
        own_item = world.get_visible(own_id)
        character = world.get_visible(other_id)
        character_room = world.get_room(character)
        own_room = world.get_room(own_item)
        if character_room == own_room or own_room in world.get_exits(character_room):
            return True
        if not inputs.get('list', False):
            inform(f"There is no {own_item.get_name()} in this room.\n")
        return False
    return interaction
