from dataclasses     import dataclass
from abc             import ABC, abstractmethod
from typing          import TypeVar, Generic

from models.state    import State, Achievement
from models.actors   import Actor, Target
from models.response import ResponseString, StaticResponse

T = TypeVar('T')

@dataclass
class RestrictionContext:
    character : Actor

class RestrictionStrategy(ABC, Generic[T]):
    @abstractmethod
    def passes(self, context:RestrictionContext, specific:T) -> tuple[bool,ResponseString]:
        pass

@dataclass
class Restriction(Generic[T]):
    specific : T
    strategy : RestrictionStrategy[T]

    def passes(self, context:RestrictionContext) -> tuple[bool,ResponseString]:
        return self.strategy.passes(context, self.specific)


@dataclass
class ItemStateContext:
    item     : Target
    state    : State
    response : str

class ItemStateRestriction(RestrictionStrategy[ItemStateContext]):
    def passes(self, context:RestrictionContext, specific:ItemStateContext) -> tuple[bool,ResponseString]:
        if specific.state in specific.item.get_current_state():
            return True, None
        return False, StaticResponse(specific.response)

@dataclass
class ItemPlacementContext:
    item     : Target
    location : Target
    response : str

class ItemPlacementRestriction(RestrictionStrategy[ItemPlacementContext]):
    def passes(self, context:RestrictionContext, specific:ItemPlacementContext) -> tuple[bool,ResponseString]:
        if not specific.item.is_in(specific.location):
            return False, specific.response
        return True, None
    
@dataclass
class CharacterAchievementContext:
    achievement : Achievement
    response    : str

class CharacterAchievementRestriciton(RestrictionStrategy[CharacterAchievementContext]):
    def passes(self, context:RestrictionContext, specific:CharacterAchievementContext) -> tuple[bool,ResponseString]:
        if context.character.has_completed_achievement(specific.achievement):
            return True, None
        return False, specific.response
