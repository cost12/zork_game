from abc         import ABC, abstractmethod
from typing      import Generic, TypeVar, TYPE_CHECKING
from dataclasses import dataclass, field

from readin.description_helpers import Description

if TYPE_CHECKING:
    from models.actors              import World, Actor
    from controls.character_control import Feedback

T = TypeVar("T")

@dataclass
class Named:
    name    : str
    name_id : str       | None = None
    aliases : list[str] | None = field(default_factory=list[str])

    def __post_init__(self):
        if not self.name_id:
            self.name_id = self.name
        self.name_id = self.name_id.lower()
        if not self.aliases:
            self.aliases = [self.name]
        self.aliases = [alias.lower() for alias in self.aliases]
        if self.name.lower() not in self.aliases:
            self.aliases.append(self.name.lower())

    def __eq__(self, other):
        return isinstance(other, Named) and other.get_id() == self.get_id()

    def __hash__(self):
        return hash(self.get_id())

    def get_name(self) -> str:
        return self.name

    def get_id(self) -> str:
        return self.name_id

    def get_aliases(self) -> list[str]:
        return self.aliases

@dataclass
class ActionContext:
    character : 'Actor'
    actions   : dict[str,'Action']

@dataclass
class Action(ABC, Named, Generic[T]):
    @abstractmethod
    def check_inputs(self, inputs:tuple) -> tuple[bool,T,Description]:
        pass

    @abstractmethod
    def take_action(self, current_state:'World', context:ActionContext, inputs:T) -> 'Feedback':
        pass

@dataclass
class Direction(Named):
    pass
