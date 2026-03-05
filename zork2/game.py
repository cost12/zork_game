import dataclasses
from abc import ABC, abstractmethod
import logging

from .world import World, WorldRules

logger = logging.getLogger(__name__)

class Player(ABC):
    @abstractmethod
    def get_character_id(self) -> str:
        pass

    @abstractmethod
    def inform(self, info: str) -> None:
        pass

    @abstractmethod
    def choose_action(self, rules: WorldRules, world: World) -> tuple[str, dict[str, str]]:
        pass

class ClPlayer(Player):
    def get_character_id(self) -> str:
        return "player1"

    def inform(self, info: str) -> None:
        print(info, end='')

    def choose_action(self, rules: WorldRules, world: World) -> tuple[str, dict[str, str]]:
        while True:
            log = world.get_log()
            action_str = input(f"S: {log.action_score(character_id=self.get_character_id())} T: {log.action_turns(character_id=self.get_character_id())} M: {log.action_count(character_id=self.get_character_id())}> ")
            actions = rules.parse_input(world.get_character(self.get_character_id()), world, action_str)
            if len(actions) == 1:
                return actions[0]
            if len(actions) > 1:
                print("This statement is ambiguous. ")
                return actions[0]
            return 'bad input', {'text': action_str}

@dataclasses.dataclass(frozen=True)
class Game:
    world : World
    rules : WorldRules
    players : tuple[Player,...]
    turn : int = 0

    def is_over(self) -> bool:
        return False

    def advance(self) -> 'Game':
        player = self.players[self.turn % len(self.players)]
        action, action_args = player.choose_action(self.rules, self.world)
        log, new_world = self.rules.advance(self.world, player.get_character_id(), action, action_args, player.inform)
        return dataclasses.replace(self, world=new_world, turn=self.turn+log.turns)
