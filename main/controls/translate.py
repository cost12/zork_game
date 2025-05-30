from typing import Any

from models.named    import Action, Named
from models.actors   import HasLocation, LocationDetail, Actor
from controls.character_control import CharacterController
from utils.relator   import NameFinder
from utils.constants import *

class Node:
    def add_edge(self, edge:str, end:'TranslateNode') -> None:
        pass

    def interpret(self, tokens:list[str], context:dict[str,list[Named]]) -> list[tuple[str,'Named|TranslateError|None',list[str],list[str],'TranslateNode|None']]:
        return []

    def get_implied(self, context:NameFinder) -> Named:
        return None

class TranslateError(Node):
    def __init__(self, message:str):
        self.message = message

class TranslateNode(Node):
    def __init__(self, state:str, edges:dict[str,'TranslateNode'], *, implied:tuple[str,str]=None):
        self.state = state
        self.edges = edges
        self.implied = implied

    def get_implied(self, context:NameFinder) -> Named:
        if self.implied is None:
            return None
        return context.get_from_input(self.implied[1], self.implied[0])[0][0]

    def add_edge(self, edge:str, end:'TranslateNode') -> None:
        self.edges[edge] = end

    def interpret(self, tokens:list[str], context:NameFinder) -> list[tuple[str,list[Named|TranslateError|None],list[str],list[str],'TranslateNode|None']]:
        if len(tokens) == 0:
            return []
        matches = list[tuple[str,Named,list[str]]]()
        for edge in self.edges:
            ms = context.get_from_input(tokens, category=edge)
            implied_token = self.edges[edge].get_implied(context)
            if implied_token is None:
                ms = [(edge,[match],tokens_used,tokens_left,self.edges[edge]) for match,tokens_used,tokens_left in ms]
            else:
                ms = [(edge,[implied_token,match],tokens_used,tokens_left,self.edges[edge]) for match,tokens_used,tokens_left in ms]
            matches.extend(ms)
        matched = len(matches) > 0
        if not matched and tokens[0] in self.edges:
            matches.append((tokens[0], None, [tokens[0]], tokens[1:], self.edges[tokens[0]]))
        elif not matched:
            return [('error', [TranslateError(f"Unexpected or unknown word: \"{tokens[0]}\".")], [tokens[0]], tokens[1:], None)]
        return matches
    
class TranslatePlacementNode(Node):
    def __init__(self, state:str, edges:dict[str,'TranslateNode']):
        self.state = state
        self.edges = edges

    def add_edge(self, edge:str, end:'TranslateNode'):
        self.edges[edge] = end

    def interpret(self, tokens:list[str], context:NameFinder) -> list[tuple[str,list[Named|TranslateError|None],list[str],list[str],'TranslateNode|None']]:
        if len(tokens) == 0:
            return []
        matches = list[tuple[str,Named,list[str]]]()
        for edge in self.edges:
            edge_matches = context.get_from_input(tokens, category=edge)
            for match,tokens_used,tokens_left in edge_matches:
                assert isinstance(match, HasLocation)
                if not isinstance(match, LocationDetail):
                    match = match.get_special_child(self.state)
                if match is not None:
                    matches.append((edge,[('placement',match)],tokens_used,tokens_left,self.edges[edge]))
        matched = len(matches) > 0
        if not matched:
            return [('error', [TranslateError(f"Unexpected or unkown word: \"{tokens[0]}\" or you can't place anything {self.state} {tokens[0]}.")], [tokens[0]], tokens[1:], None)]
        return matches

class Translator:

    def __init__(self, head:Node, *, remove=None):
        self.head = head
        self.remove = list[str]() if remove is None else remove
        self.remove = [token.lower() for token in self.remove]

    def __clean(self, input:str) -> list[str]:
        cleaned = input.lower().split()
        cleaned = [token for token in cleaned if token not in self.remove]
        cleaned.append('\n')
        return cleaned

    def interpret(self, input:str, name_space:NameFinder, character:Actor, controller:CharacterController) -> tuple[Action,tuple]:
        tokens = self.__clean(input)
        translation = list[Named]()
        result = self.head.interpret(tokens, name_space)
        while len(result) > 0:
            if len(result) > 1:
                # pick one
                room = character.get_top_parent()
                in_room = []
                for edge,translated_tokens,tokens_used,tokens_left,next_node in result:
                    for token in translated_tokens:
                        if room.contains_item(token):
                            in_room.append((edge,translated_tokens,tokens_used,tokens_left,next_node))
                            break
                if len(in_room) >= 1:
                    result = in_room
                if len(result) > 1:
                    index = controller.decide([(translated_tokens,tokens_used) for _,translated_tokens,tokens_used,_,_ in result])
                    result = [result[index]]
                if DEBUG_INPUT: print(result)
                pass
            edge, translated_tokens, tokens_used, tokens_left, next_node = result[0]
            if translated_tokens is not None:
                translation.extend(translated_tokens)
            if next_node is None:
                break
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
    placement_leaf = TranslateNode('placement', {})
    placement = TranslateNode('placement', {"\n": placement_leaf})
    placement_in = TranslatePlacementNode('inside', {
        'target'         : placement,
        'locationdetail' : placement,
        'actor'          : placement
    })
    placement_on = TranslatePlacementNode('on', {
        'target'         : placement,
        'locationdetail' : placement,
        'actor'          : placement
    })
    target = TranslateNode('target', {'\n':action_input_leaf, 'on':placement_on, 'in':placement_in})
    action = TranslateNode('action', {
        'target'    :target,
        'direction' :target,
        'location'  :target,
        'path'      :target,
        'actor'     :target,
        '\n'        :action_leaf
    })
    direction_leaf = TranslateNode('direction', {})
    direction = TranslateNode('direction', {'\n':direction_leaf}, implied=('action', 'go'))
    start_error = TranslateError('No command given.')
    standard_input = TranslateNode('start', {
        'action'    :action,
        'direction' :direction,
        '\n'        :start_error
    })
    return Translator(standard_input, remove=['a','an','the','i'])