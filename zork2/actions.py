from typing import Callable

from .world import World, WorldRules, ActionLogLine

def bad_input() -> Callable[[str,WorldRules,World,str,dict[str,str],Callable[[str],None]],tuple[bool, World]]:
    def action(own_id: str, rules: WorldRules, world: World, character_id: str, inputs: dict[str,str], inform: Callable[[str],None]) -> tuple[bool,World]:
        character = world.get_character(character_id)
        new_world = world.update_log(ActionLogLine(character_id, world.get_room(character).get_id(), own_id, False))
        return False, new_world
    return action

def look() -> Callable[[str,WorldRules,World,str,dict[str,str],Callable[[str],None]],tuple[bool, World]]:
    def action(own_id: str, rules: WorldRules, world: World, character_id: str, inputs: dict[str,str], inform: Callable[[str],None]) -> tuple[bool,World]:
        character = world.get_character(character_id)
        if inputs.get('target', None) in [None, '__parent']:
            target = world.get_parent(character)
        else:
            target = world.get_visible(inputs['target'])
        if character.can_interact_with(rules, world, target.get_id(), own_id, inform):
            inform(f"[{target.get_name()}]")
            target.describe(rules, world, character_id, inform)
            new_world = world.update_log(ActionLogLine(character_id, world.get_room(character).get_id(), own_id, True))
            return True, new_world
        new_world = world.update_log(ActionLogLine(character_id, world.get_room(character).get_id(), own_id, False))
        return False, new_world
    return action

def walk() -> Callable[[str,WorldRules,World,str,dict[str,str],Callable[[str],None]],tuple[bool, World]]:
    def action(own_id: str, rules: WorldRules, world: World, character_id: str, inputs: dict[str,str], inform: Callable[[str],None]) -> tuple[bool,World]:
        own_action = world.get_action(own_id)
        inform("walking")
        return False, world
    return action
