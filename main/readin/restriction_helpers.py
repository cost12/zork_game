from dataclasses     import dataclass
from abc             import ABC, abstractmethod
from typing          import TypeVar, Generic

from models.state    import State, Achievement
from models.actors   import Actor, Target, ItemTree
from readin.description_helpers import Description, PlainTextContext, PlainTextDescription
T = TypeVar('T')

@dataclass
class RestrictionContext:
    character : Actor
    inventory : ItemTree

class RestrictionStrategy(ABC, Generic[T]):
    @abstractmethod
    def passes(self, context:RestrictionContext, specific:T) -> tuple[bool,Description]:
        pass

@dataclass
class Restriction(Generic[T]):
    specific : T
    strategy : RestrictionStrategy[T]

    def passes(self, context:RestrictionContext) -> tuple[bool,Description]:
        return self.strategy.passes(context, self.specific)


@dataclass
class ItemStateContext:
    item     : Target
    state    : State
    response : Description

class ItemStateRestriction(RestrictionStrategy[ItemStateContext]):
    def passes(self, context:RestrictionContext, specific:ItemStateContext) -> tuple[bool,Description]:
        if specific.state in specific.item.get_current_state():
            return True, None
        return False, specific.response

@dataclass
class ItemPlacementContext:
    item     : Target
    location : Target
    response : Description

class ItemPlacementRestriction(RestrictionStrategy[ItemPlacementContext]):
    def passes(self, context:RestrictionContext, specific:ItemPlacementContext) -> tuple[bool,Description]:
        if not specific.item.is_in(specific.location):
            return False, specific.response
        return True, None

@dataclass
class CharacterAchievementContext:
    achievement : Achievement
    response    : Description

class CharacterAchievementRestriciton(RestrictionStrategy[CharacterAchievementContext]):
    def passes(self, context:RestrictionContext, specific:CharacterAchievementContext) -> tuple[bool,Description]:
        if context.character.has_completed_achievement(specific.achievement):
            return True, None
        return False, specific.response

@dataclass
class CharacterWearingContext:
    item     : Target
    response : str

class CharacterWearingRestriciton(RestrictionStrategy[CharacterWearingContext]):
    def passes(self, context:RestrictionContext, specific:CharacterWearingContext) -> tuple[bool,Description]:
        if context.inventory.is_wearing(context.character, specific.item):
            return True, None
        return False, Description[PlainTextContext](None, PlainTextContext(specific.response), PlainTextDescription())
