from typing import Any

from models.named    import Action, Named
from utils.relator   import NameFinder
from utils.constants import *

class Node:
    def add_edge(self, edge:str, end:'TranslateNode') -> None:
        pass

    def interpret(self, tokens:list[str], context:dict[str,list[Named]]) -> list[tuple[str,'Named|TranslateError|None',list[str],list[str],'TranslateNode|None']]:
        pass

class TranslateError(Node):
    def __init__(self, message:str):
        self.message = message

    def interpret(self, tokens:list[str], context:dict[str,list[Named]]) -> list[tuple[str,'Named|TranslateError|None',list[str],list[str],'TranslateNode|None']]:
        return []

class TranslateNode(Node):
    def __init__(self, state:str, edges:dict[str,'TranslateNode']):
        self.state = state
        self.edges = edges

    def add_edge(self, edge:str, end:'TranslateNode') -> None:
        self.edges[edge] = end

    def interpret(self, tokens:list[str], context:NameFinder) -> list[tuple[str,Named|TranslateError|None,list[str],list[str],'TranslateNode|None']]:
        if len(tokens) == 0:
            return []
        matches = list[tuple[str,Named,list[str]]]()
        for edge in self.edges:
            ms = context.get_from_input(tokens, category=edge)
            ms = [(edge,match,tokens_used,tokens_left,self.edges[edge]) for match,tokens_used,tokens_left in ms]
            matches.extend(ms)
        matched = len(matches) > 0
        if not matched and tokens[0] in self.edges:
            matches.append((tokens[0], None, [tokens[0]], tokens[1:], self.edges[tokens[0]]))
        elif not matched:
            return [('error', TranslateError(f"Unexpected or unknown word: \"{tokens[0]}\""), [tokens[0]], tokens[1:], None)]
        return matches

class Translator:

    def __init__(self, head:Node):
        self.head = head

    def interpret(self, input:str, name_space:NameFinder) -> tuple[Action,tuple]:
        tokens = input.lower().split()
        tokens.append('\n')
        translation = list[Named]()
        result = self.head.interpret(tokens, name_space)
        while len(result) > 0:
            if len(result) > 1:
                # pick one
                print("Ambiguous meaning, guessing at random...")
                if DEBUG_INPUT: print(result)
                pass
            edge, translated_token, tokens_used, tokens_left, next_node = result[0]
            if translated_token is not None:
                translation.append(translated_token)
            if next_node is None:
                result = []
            else:
                result = next_node.interpret(tokens_left, name_space)
        for token in translation:
            if isinstance(token, TranslateError):
                return "error", token
        if len(translation) == 0:
            return "error", TranslateError("Please say something")
        return translation[0], translation[1:]
    
def get_input_translator() -> Translator:
    action_leaf = TranslateNode('action', {})
    action_input_leaf = TranslateNode('action_input', {})
    target = TranslateNode('target', {'\n':action_input_leaf})
    action = TranslateNode('action', {'target':target,
                                      'direction':target,
                                      'location':target,
                                      'path':target,
                                      'actor':target,
                                      '\n':action_leaf})
    action.add_edge('the',action)
    action.add_edge('a',action)
    start_error = TranslateError('No command given.')
    start = TranslateNode('start', {'action':action,'\n':start_error})
    start.add_edge('i',start)
    return Translator(start)