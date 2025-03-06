from typing import Any

from code.models.action import Action
from code.models.item import Item
from code.models.room import Direction, Room, Exit
from code.models.character import Character
from code.utils.alias import Alias

class Node:
    def add_edge(self, edge:str, end:'TranslateNode') -> None:
        pass

    def interpret(self, tokens:list[str], context:dict[str,list[Alias]]) -> tuple:
        pass

class TranslateError(Node):
    def __init__(self, message:str):
        self.message = message

    def interpret(self, tokens:list[str], context:dict[str,list[Alias]]) -> tuple:
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

    def interpret(self, input:str, actions:dict[str,Action], characters:dict[str,Character], rooms:dict[str,Room], items:dict[str,Item], directions:dict[str,Direction]) -> tuple[Action,tuple]:
        context = {
            'action'    : actions,
            'character' : characters,
            'room'      : rooms,
            'item'      : items,
            'direction' : directions
        }
        tokens = input.split()
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