from typing import Callable

from .world import World, WorldRules, ActionLogLine

def bad_input() -> Callable[[str,WorldRules,World,str,dict[str,str],Callable[[str],None]],tuple[bool, World]]:
    def action(own_id: str, rules: WorldRules, world: World, character_id: str, inputs: dict[str,str], inform: Callable[[str],None]) -> tuple[ActionLogLine,World]:
        character = world.get_character(character_id)
        log = ActionLogLine(character_id, world.get_room(character).get_id(), own_id, False, 0)
        new_world = world.update_log(log)
        return log, new_world
    return action

def debug() -> Callable[[str,WorldRules,World,str,dict[str,str],Callable[[str],None]],tuple[bool, World]]:
    def action(own_id: str, rules: WorldRules, world: World, character_id: str, inputs: dict[str,str], inform: Callable[[str],None]) -> tuple[ActionLogLine,World]:
        inform(f"{str(world)}\n")
        character = world.get_character(character_id)
        log = ActionLogLine(character_id, world.get_room(character).get_id(), own_id, True, 0)
        new_world = world.update_log(log)
        return log, new_world
    return action

def look() -> Callable[[str,WorldRules,World,str,dict[str,str],Callable[[str],None]],tuple[bool, World]]:
    def action(own_id: str, rules: WorldRules, world: World, character_id: str, inputs: dict[str,str], inform: Callable[[str],None]) -> tuple[ActionLogLine,World]:
        character = world.get_character(character_id)
        if inputs.get('target', None) in [None, '__parent']:
            target = world.get_parent(character)
        else:
            target = world.get_visible(inputs['target'])
        if character.can_interact_with(rules, world, target.get_id(), own_id, {}, inform):
            inform(f"[{target.get_name()}]\n")
            target.describe(rules, world, character_id, {}, inform)
            log = ActionLogLine(character_id, world.get_room(character).get_id(), own_id, True, 0)
            new_world = world.update_log(log)
            return log, new_world
        log = ActionLogLine(character_id, world.get_room(character).get_id(), own_id, False, 0)
        new_world = world.update_log(log)
        return log, new_world
    return action

def walk() -> Callable[[str,WorldRules,World,str,dict[str,str],Callable[[str],None]],tuple[bool, World]]:
    def action(own_id: str, rules: WorldRules, world: World, character_id: str, inputs: dict[str,str], inform: Callable[[str],None]) -> tuple[ActionLogLine,World]:
        character = world.get_character(character_id)
        character_room = world.get_room(character)
        direction_id = inputs.get('direction', None)
        if direction_id is None:
            inform("No direction was given.")
            log = ActionLogLine(character_id, character_room.get_id(), own_id, False, 0)
            new_world = world.update_log(log)
            return log, new_world
        path = world.get_path(character_room, world.get_direction(direction_id))
        if path and path.can_interact_with(rules, world, character_id, own_id, {}, inform):
            new_room_id = path.get_end()
            new_room = world.get_visible(new_room_id)
            new_world = world.move_item(character, new_room)
            new_room.describe(rules, new_world, character_id, {"from_walk": True}, inform)
            log = ActionLogLine(character_id, character_room.get_id(), own_id, True, 1)
            new_world = new_world.update_log(log)
            return log, new_world
        if path is None:
            inform("You foolishly walk straight into a wall thinking there might be a path there. Ouch.\n")
        log = ActionLogLine(character_id, world.get_room(character).get_id(), own_id, False, 0)
        new_world = world.update_log(log)
        return log, new_world
    return action
