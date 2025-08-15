"""Commonly used functions in Target descriptions"""

from dataclasses   import dataclass
from abc           import ABC, abstractmethod
from typing        import TypeVar, Generic

from models.named  import Action
from models.state  import State
from models.actors import Actor, Target
from utils.utils   import list_to_str

T = TypeVar("T")

@dataclass
class DescriptionContext:
    action    : Action
    success   : bool
    character : Actor
    target    : Target
    tool      : Target
    described : Target

class DescriptionStrategy(ABC, Generic[T]):
    @abstractmethod
    def describe(self, context:DescriptionContext, specific:T) -> str:
        pass

@dataclass
class Description(Generic[T]):
    specific : T
    strategy : DescriptionStrategy

    def describe(self, context:DescriptionContext) -> str:
        return self.strategy.describe(context, self.specific)


@dataclass
class PlainTextContext:
    text : str

class PlainTextDescription(DescriptionStrategy[PlainTextContext]):
    def describe(self, context:DescriptionContext, specific:PlainTextContext) -> str:
        return specific.text

def plain_text_description(description:str) -> Description[PlainTextContext]:
    return Description[PlainTextContext](PlainTextContext(description), PlainTextDescription())

@dataclass
class ContentsContext:
    full_text  : str
    empty_text : str

class ContentsDescription(DescriptionStrategy[ContentsContext]):
    def describe(self, context:DescriptionContext, specific:ContentsContext) -> str:
        contents = context.described.list_contents_visible_to(context.character)
        if len(contents) == 0:
            return specific.empty_text
        return f"{specific.full_text} {list_to_str([item.get_description_to(context.character) for item in contents])}"

@dataclass
class StateContext:
    state_responses : dict[State,str]

class StateDescription(DescriptionStrategy[ContentsContext]):
    def describe(self, context:DescriptionContext, specific:StateContext) -> str:
        description = ""
        for state in context.described.get_current_state():
            if state in specific.state_responses:
                description += specific.state_responses[state]
        return description

@dataclass
class CombinationContext:
    descriptions : list[Description]
    joiner       : str = '\n'

class CombinationDescription(DescriptionStrategy[CombinationContext]):
    def describe(self, context:DescriptionContext, specific:CombinationContext) -> str:
        return specific.joiner.join([description.describe(context) for description in specific.descriptions])
