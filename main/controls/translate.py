from typing import Any, Optional

from models.action import Action, Named
from models.actors import Direction, Location, Path, Target, Actor
from factories.factories import ItemFactory, NamedFactory, StateFactory, LocationFactory, SkillSetFactory, CharacterFactory, StateGraphFactory, LocationDetailFactory, CharacterControlFactory, StateDisconnectedGraphFactory

class Word:
    def __init__(self):
        pass

class InputDictionary:

    def __init__(self, dictionary:dict[str,dict[str,Any]]):
        self.dictionary = dictionary

    def translate(self, token:str) -> Word:
        pass

    def translate_str(self, input_str:str) -> list[Word]:
        pass

class Node:
    def add_edge(self, edge:str, end:'TranslateNode') -> None:
        pass

    def interpret(self, tokens:list[str], context:dict[str,list[Named]]) -> tuple:
        pass

class TranslateError(Node):
    def __init__(self, message:str):
        self.message = message

    def interpret(self, tokens:list[str], context:dict[str,list[Named]]) -> tuple:
        return (self,)

class TranslateNode(Node):
    def __init__(self, state:str, edges:dict[str,'TranslateNode']):
        self.state = state
        self.edges = edges

    def add_edge(self, edge:str, end:'TranslateNode') -> None:
        self.edges[edge] = end

    def interpret(self, tokens:list[str], context:dict[str,dict[str,Any]]) -> tuple:
        if len(tokens) == 0:
            return (None,)
        value = None
        edge = None
        token = tokens[0]
        matched = False
        for e,dictionary in context.items():
            if e in self.edges:
                if token in dictionary:
                    value = dictionary[token]
                    edge = e
                    matched = True
        if not matched and token in self.edges:
            value = None
            edge = token
        elif not matched:
            return (TranslateError(f"Unexpected or unknown word: \"{token}\""),)
        if value is None:
            return self.edges[edge].interpret(tokens[1:], context)
        else:
            return value, *self.edges[edge].interpret(tokens[1:], context)
        
class Translator:

    def __init__(self, head:Node):
        self.head = head

    def interpret(self, input:str, actions:dict[str,Action], characters:dict[str,Actor], rooms:dict[str,Location], items:dict[str,Target], directions:dict[str,Direction]) -> tuple[Action,tuple]:
        context = {
            'action'    : actions,
            'character' : characters,
            'room'      : rooms,
            'item'      : items,
            'direction' : directions
        }
        tokens = input.lower().split()
        tokens.append('\n')
        result = self.head.interpret(tokens, context)
        for token in result:
            if isinstance(token, TranslateError):
                return "error", token
        return result[0], result[1:-1]
    
def get_input_translator() -> Translator:
    action_leaf = TranslateNode('action', {})
    action_input_leaf = TranslateNode('action_input', {})
    target = TranslateNode('target', {'\n':action_input_leaf})
    action = TranslateNode('action', {'item':target,
                                      'direction':target,
                                      'room':target,
                                      'exit':target,
                                      'character':target,
                                      '\n':action_leaf})
    action.add_edge('the',action)
    action.add_edge('a',action)
    start_error = TranslateError('No command given.')
    start = TranslateNode('start', {'action':action,'\n':start_error})
    start.add_edge('i',start)
    return Translator(start)