"""Commonly used functions in Target descriptions"""

from dataclasses   import dataclass
from abc           import ABC, abstractmethod
from typing        import TypeVar, Generic, TYPE_CHECKING

from models.named  import Action
from models.state  import State
from models.actors import Actor, Target, HasLocation
from utils.utils   import list_to_str

if TYPE_CHECKING:
    from models.actors import ItemTree
    from readin.restriction_helpers import RestrictionContext

T = TypeVar("T")

@dataclass
class DescriptionContext:
    placements : 'ItemTree'
    action     : Action
    success    : bool
    character  : Actor
    target     : Target
    tool       : Target

class DescriptionStrategy(ABC, Generic[T]):
    @abstractmethod
    def describe(self, described:HasLocation, context:DescriptionContext, specific:T) -> str:
        pass

@dataclass
class Description(Generic[T]):
    described : HasLocation
    specific  : T
    strategy  : DescriptionStrategy

    def describe(self, context:DescriptionContext) -> str:
        return self.strategy.describe(self.described, context, self.specific)

@dataclass
class PlainTextContext:
    text : str

class PlainTextDescription(DescriptionStrategy[PlainTextContext]):
    def describe(self, described:HasLocation, context:DescriptionContext, specific:PlainTextContext) -> str:
        return specific.text

def plain_text_description(description:str) -> Description[PlainTextContext]:
    return Description[PlainTextContext](None, PlainTextContext(description), PlainTextDescription())

@dataclass
class ContentsContext:
    item_tree  : 'ItemTree'
    full_text  : str
    empty_text : str

class ContentsDescription(DescriptionStrategy[ContentsContext]):
    def describe(self, described:HasLocation, context:DescriptionContext, specific:ContentsContext) -> str:
        contents = context.placements.get_children(described)
        if len(contents) == 0:
            return specific.empty_text
        return (
            f"{specific.full_text} ",
            f"{list_to_str([
                (
                    item
                    .describe(RestrictionContext(context.character, specific.item_tree))
                    .describe(context.character)
                    for item in contents
                )
            ])}"
        )

@dataclass
class StateContext:
    state_responses : dict[State,str]

class StateDescription(DescriptionStrategy[ContentsContext]):
    def describe(self, described:Target, context:DescriptionContext, specific:StateContext) -> str:
        description = ""
        for state in described.get_current_state():
            if state in specific.state_responses:
                description += specific.state_responses[state]
        return description

@dataclass
class CombinationContext:
    descriptions : list[Description]
    joiner       : str = '\n'

class CombinationDescription(DescriptionStrategy[CombinationContext]):
    def describe(self, described:HasLocation, context:DescriptionContext, specific:CombinationContext) -> str:
        return specific.joiner.join([description.describe(context) for description in specific.descriptions])

def combine_descriptions(descriptions:list[Description], *, joiner:str='\n') -> Description[CombinationContext]:
    return Description[CombinationContext](
        None,
        CombinationContext(
            [description for description in descriptions if description is not None],
            joiner=joiner
        ),
        CombinationDescription()
    )


class BackupDescription(DescriptionStrategy[list[Description]]):
    def describe(self, described:HasLocation, context:DescriptionContext, specific:list[Description]):
        for description in specific:
            desc_str = description.describe(context)
            if desc_str:
                return desc_str
        return None

def backup_description(descriptions:list[Description],) -> Description[list[Description]]:
    return Description[list[Description]](
        None,
        descriptions,
        BackupDescription()
    )
