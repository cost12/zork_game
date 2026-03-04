from typing import Callable

from .world import World, WorldRules

def simple_interaction() -> Callable[[str,WorldRules,World,str,str,Callable[[str],None]],bool]:
    def interaction(own_id: str, rules: WorldRules, world: World, character_id: str, action_id: str, inform: Callable[[str],None]) -> bool:
        own_item = world.get_visible(own_id)
        character = world.get_character(character_id)
        if world.get_room(character) == world.get_room(own_item):
            return True
        inform(f"There is no {own_item.get_name()} in this room.")
        return False
    return interaction
