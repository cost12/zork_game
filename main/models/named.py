from abc         import ABC, abstractmethod
from typing      import Generic, TypeVar, TYPE_CHECKING
from dataclasses import dataclass, field

from frozendict import frozendict

if TYPE_CHECKING:
    from models.actors              import World, Actor
    from controls.character_control import Feedback
    from readin.description_helpers import Description

T = TypeVar("T")

@dataclass(frozen=True)
class Named:
    name    : str
    name_id : str|None = None
    aliases : tuple[str,...]|None = field(default_factory=tuple)

    def __post_init__(self):
        if not self.name_id:
            object.__setattr__(self, 'name_id', self.name)
        object.__setattr__(self, 'name_id', self.name_id.lower())
        if not self.aliases:
            object.__setattr__(self, 'aliases', (self.name,))
        new_aliases = [alias.lower() for alias in self.aliases]
        if self.name.lower() not in self.aliases:
            new_aliases.append(self.name.lower())
        object.__setattr__(self, 'aliases', tuple(new_aliases))

    def get_name(self) -> str:
        return self.name

    def get_id(self) -> str:
        return self.name_id

    def get_aliases(self) -> list[str]:
        return list(self.aliases)

@dataclass(frozen=True)
class ActionContext:
    character : 'Actor'
    actions   : frozendict[str,'Action']

@dataclass(frozen=True)
class Action(ABC, Named, Generic[T]):
    @abstractmethod
    def check_inputs(self, inputs:tuple) -> tuple[bool,T,'Description']:
        pass

    @abstractmethod
    def take_action(self, current_state:'World', context:ActionContext, inputs:T) -> 'Feedback':
        pass

@dataclass(frozen=True)
class Direction(Named):
    pass
