import dataclasses
from abc import ABC, abstractmethod
import logging

from .world import World, WorldRules, Action
from .utils import Named

logger = logging.getLogger(__name__)

class Player(ABC):
    @abstractmethod
    def get_character_id(self) -> str:
        pass

    @abstractmethod
    def take_action(self, rules: WorldRules, world: World) -> tuple[str, dict[str, Named]]:
        pass

class ClPlayer(Player):
    def get_character_id(self) -> str:
        return "player1"

    def take_action(self, rules: WorldRules, world: World) -> tuple[str, dict[str, Named]]:
        while True:
            action_str = input("What do you do? ")
            actions = rules.parse_input(world.get_character(self.get_character_id()), world, action_str)
            if len(actions) == 1:
                return actions[0]
            if len(actions) > 1:
                logger.debug("ambiguous meaning")
                return actions[0]
            logger.debug("bad input")

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
        action, action_args = player.take_action(self.rules, self.world)
        success, new_world = self.rules.advance(self.world, player.get_character_id(), action, action_args)
        if success:
            return dataclasses.replace(self, world=new_world, turn=self.turn+1)
        return self
