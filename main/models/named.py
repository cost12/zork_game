from abc         import ABC, abstractmethod
from typing      import Any, Generic, TypeVar, TYPE_CHECKING
from dataclasses import dataclass

from readin.description_helpers import DescriptionStrategy, Description
from readin.restriction_helpers import RestrictionContext

if TYPE_CHECKING:
    from models.actors              import World, Actor
    from controls.character_control import Feedback


T = TypeVar("T")

class NameInfo:

    def __init__(self, name:str, description_context:Any, description_strategy:DescriptionStrategy, *, name_id:str=None, aliases:list[str]=None):
        self.name                 = name
        self.description_context  = description_context
        self.description_strategy = description_strategy
        self.name_id              = name if name_id is None else name_id
        self.name_id              = self.name_id.lower()
        self.aliases              = [self.name.lower()] if aliases is None else [alias.lower() for alias in aliases]
        if self.name.lower() not in self.aliases:
            self.aliases.append(self.name.lower())

class Named:

    def __init__(self, name_info:NameInfo):
        self.name_info = name_info

    def __repr__(self):
        return f"<Named: {self.get_name()}>"

    def __eq__(self, other):
        return isinstance(other, Named) and other.get_id() == self.get_id()

    def __hash__(self):
        return hash(self.get_id())

    def get_name(self) -> str:
        return self.name_info.name

    def get_id(self) -> str:
        return self.name_info.name_id

    def get_aliases(self) -> list[str]:
        return self.name_info.aliases

    def describe(self, context:RestrictionContext) -> Description:
        return Description(self, self.name_info.description_context, self.name_info.description_strategy)

@dataclass
class ActionContext:
    character : 'Actor'
    actions   : dict[str,'Action']

class Action(ABC, Named, Generic[T]):

    def __repr__(self):
        return f"<Action: {self.get_name()}>"

    @abstractmethod
    def check_inputs(self, inputs:tuple) -> tuple[bool,T,Description]:
        pass

    @abstractmethod
    def take_action(self, current_state:'World', context:ActionContext, inputs:T) -> 'Feedback':
        pass

class Direction(Named):

    def __repr__(self):
        return f"<Direction {self.get_name()}>"
