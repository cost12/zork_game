from typing import Callable

from .world import World, WorldRules

def look() -> Callable[[str,WorldRules,World,str,dict[str,str],Callable[[str],None]],tuple[bool, World]]:
    def action(own_id: str, rules: WorldRules, world: World, character_id: str, inputs: dict[str,str], inform: Callable[[str],None]) -> tuple[bool,World]:
        own_action = world.get_action(own_id)
        inform("looking")
        return False, world
    return action

def walk() -> Callable[[str,WorldRules,World,str,dict[str,str],Callable[[str],None]],tuple[bool, World]]:
    def action(own_id: str, rules: WorldRules, world: World, character_id: str, inputs: dict[str,str], inform: Callable[[str],None]) -> tuple[bool,World]:
        own_action = world.get_action(own_id)
        inform("walking")
        return False, world
    return action
