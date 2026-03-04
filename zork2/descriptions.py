from typing import Callable

from .world import World, WorldRules

def plain_text(text: str) -> Callable[[str,WorldRules,World,str,Callable[[str],None]],None]:
    def description(own_id: str, rules: WorldRules, world: World, character_id: str, inform: Callable[[str],None]) -> str:
        own_item = world.get_visible(own_id)
        if own_item.can_interact_with(rules, world, character_id, 'look', inform):
            inform(text)
    return description
