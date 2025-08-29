from typing import Callable, Any

from utils.relator    import NameFinder
from models.named     import NameInfo, Action
from controls.actions import DropAction, LookAction, TakeAction, WaitAction, WalkAction, DefaultAction, CheckInventoryAction

def get_action(constructor:Callable[[Any],Action], name:str, aliases:list[str], **kwargs):
    return constructor(NameInfo(name=name, description_context=None, description_strategy=None, aliases=aliases, **kwargs))

def add_to_name_space(name_space:NameFinder) -> None:
    actions = [
        get_action(LookAction, "look", ["look", "inspect", "search", "look around", "investigate", "stare"])
    ]
    actions = [
		get_action(TakeAction,           name = "take",      aliases = ["take", "grab", "pick up"],        inventory="inventory", cant_take_text="You can't take",         empty_take_text="Take what?",     full_pack_text="doesn't fit in your inventory.",     taken_text="Taken.", not_taken_text="No items were taken."),
		get_action(TakeAction,           name = "wear",      aliases = ["put on", "wear", "don"],          inventory="wearing",   cant_take_text="You can't wear",         empty_take_text="Wear what?",     full_pack_text="doesn't fit over your many layers.", taken_text="Worn.",  not_taken_text="No items were worn."),
		get_action(DropAction,           name = "drop",      aliases = ["drop", "let go", "put", "place"], inventory="inventory", cant_drop_text="You can't drop",         empty_drop_text="Drop what?",     dropped_text="Dropped.", no_drop_text="No items were dropped."),
		get_action(DropAction,           name = "take off",  aliases = ["take off", "remove", "doff"],     inventory="wearing",   cant_drop_text="You can't take off",     empty_drop_text="Take off what?", dropped_text="Dropped.", no_drop_text="No items were taken off."),
		get_action(CheckInventoryAction, name = "inventory", aliases = ["inventory", "check inventory"],   inventory="inventory", contains_text="Your inventory contains", empty_text="Your inventory is empty."),
		get_action(CheckInventoryAction, name = "wearing",   aliases = ["wearing"],                        inventory="wearing",   contains_text="You are wearing",         empty_text="You have nothing on but the clothes you woke up in."),
		get_action(LookAction,    name = "look",        aliases = ["look", "inspect", "search", "look around", "investigate", "stare"]),
		get_action(WaitAction,    name = "wait",        aliases = ["wait", "chill", "relax"]),
		get_action(WalkAction,    name = "walk",        aliases = ["walk","go","g","head","proceed","run", "advance", "strut", "meander"]),
		get_action(DefaultAction, name = "hang",        aliases = ["hang"]),
		get_action(DefaultAction, name = "break",       aliases = ["break", "shatter", "smash"]),
		get_action(DefaultAction, name = "turn on",     aliases = ["turn on"]),
		get_action(DefaultAction, name = "turn off",    aliases = ["turn off"]),
		get_action(DefaultAction, name = "toggle",      aliases = ["toggle", "switch", "flip"]),
		get_action(DefaultAction, name = "attack",      aliases = ["slay","kill","fight","cut","attack","hit","strike", "assault"]),
		get_action(DefaultAction, name = "play",        aliases = ["play"]),
		get_action(DefaultAction, name = "conduct",     aliases = ["conduct"]),
		get_action(DefaultAction, name = "eat",         aliases = ["eat"]),
		get_action(DefaultAction, name = "drink",       aliases = ["drink", "chug"]),
		get_action(DefaultAction, name = "dig",         aliases = ["dig"]),
		get_action(DefaultAction, name = "shoot",       aliases = ["shoot", "throw", "toss"]),
		get_action(DefaultAction, name = "bounce",      aliases = ["bounce", "dribble"]),
		get_action(DefaultAction, name = "give",        aliases = ["give", "offer", "share"]),
		get_action(DefaultAction, name = "burn",        aliases = ["burn", "torch", "set on fire", "light", "ignite"]),
		get_action(DefaultAction, name = "extinguish",  aliases = ["put out", "extinguish"]),
		get_action(DefaultAction, name = "unlock",      aliases = ["unlock"]),
		get_action(DefaultAction, name = "lock",        aliases = ["lock"]),
		get_action(DefaultAction, name = "open",        aliases = ["open"]),
		get_action(DefaultAction, name = "close",       aliases = ["close", "shut"]),
		get_action(DefaultAction, name = "say",         aliases = ["say", "speak", "whisper", "yell"]),
		get_action(DefaultAction, name = "arm wrestle", aliases = ["arm wrestle"]),
		get_action(DefaultAction, name = "work on",     aliases = ["work on"]),
		get_action(DefaultAction, name = "read",        aliases = ["read"]),
		get_action(DefaultAction, name = "type",        aliases = ["type"]),
		get_action(DefaultAction, name = "tie",         aliases = ["tie"]),
		get_action(DefaultAction, name = "untie",       aliases = ["untie"]),
		get_action(DefaultAction, name = "fill",        aliases = ["fill"]),
		get_action(DefaultAction, name = "empty",       aliases = ["empty", "drain"]),
		get_action(DefaultAction, name = "admire",      aliases = ["admire"]),
		get_action(DefaultAction, name = "squeeze",     aliases = ["squeeze"]),
		get_action(DefaultAction, name = "ride",        aliases = ["ride"]),
		get_action(DefaultAction, name = "perform",     aliases = ["do", "perform"]),
		get_action(DefaultAction, name = "lift",        aliases = ["lift"]),
		get_action(DefaultAction, name = "pour",        aliases = ["pour"]),
		get_action(DefaultAction, name = "hug",         aliases = ["hug"]),
		get_action(DefaultAction, name = "kiss",        aliases = ["kiss"]),
		get_action(DefaultAction, name = "compliment",  aliases = ["compliment"]),
    ]

    name_space.add_many(actions)
