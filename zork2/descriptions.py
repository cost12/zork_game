from typing import Callable

from .world import World, WorldRules

def plain_text(text: str, list_text: str) -> Callable[[str,WorldRules,World,str,dict[str,str],Callable[[str],None]],None]:
    def description(own_id: str, rules: WorldRules, world: World, character_id: str, inputs: dict[str,str], inform: Callable[[str],None]) -> str:
        own_item = world.get_visible(own_id)
        if own_item.can_interact_with(rules, world, character_id, 'look', inputs, inform):
            if inputs.get('list', False):
                inform(list_text)
            else:
                inform(f"{text}\n")
    return description

def room_description(text: str, contents_text: str) -> Callable[[str,WorldRules,World,str,dict[str,str],Callable[[str],None]],None]:
    def description(own_id: str, rules: WorldRules, world: World, character_id: str, inputs: dict[str,str], inform: Callable[[str],None]) -> str:
        own_item = world.get_visible(own_id)
        if own_item.can_interact_with(rules, world, character_id, 'look', inputs, inform):
            if inputs.get('from_walk', False):
                inform(f"[{own_item.get_name()}]\n")
            inform(f"{text} ")
            for path in world.get_exits(own_item):
                path.describe(rules, world, character_id, inputs | {"from_room": True}, inform)
            children = world.get_children(own_item)
            character = world.get_character(character_id)
            if character in children:
                children.remove(character)
            if len(children) > 0:
                inform(f"{contents_text} ")
                for child in children:
                    child.describe(rules, world, character_id, inputs | {"list": True}, inform)
                inform(".")
            inform("\n")
    return description

def path_description(text: str, from_room_text: str, contents_text: str) -> Callable[[str,WorldRules,World,str,dict[str,str],Callable[[str],None]],None]:
    def description(own_id: str, rules: WorldRules, world: World, character_id: str, inputs: dict[str,str], inform: Callable[[str],None]) -> str:
        own_item = world.get_visible(own_id)
        if own_item.can_interact_with(rules, world, character_id, 'look', inputs, inform):
            character = world.get_character(character_id)
            if inputs.get('from_room', False):
                character_room = world.get_room(character)
                direction = world.get_path_direction(character_room, own_item)
                inform(from_room_text.format(direction=direction.get_name()))
            else:
                inform(f"{text} ")
            children = world.get_children(own_item)
            if character in children:
                children.remove(character)
            if len(children) > 0:
                inform(f"{contents_text} ")
                for child in children:
                    child.describe(rules, world, character_id, inputs | {"list": True}, inform)
                inform(".")
            if inputs.get('from_room', False):
                inform(" ")
            else:
                inform("\n")
    return description
