from dataclasses import dataclass

import views.string_views as views

@dataclass(frozen=True)
class Feedback:
    feedback:str
    success:bool=True
    moves:int=1
    turns:int=1
    score:int=0

    def as_string(self) -> str:
        return self.feedback

class CharacterController:

    def __init__(self):
        pass

    def make_move(self) -> str:
        pass

    def feedback(self, feedback:Feedback) -> None:
        pass

class NPCController(CharacterController):
    def __init__(self):
        pass

    def make_move(self) -> str:
        return 'wait'

    def feedback(self, feedback:Feedback) -> None:
        pass

class CommandLineController(CharacterController):

    def __init__(self):
        self.moves = 0
        self.turns = 0
        self.score = 0

    def make_move(self) -> str:
        return input(views.input_prompt(self.moves,self.turns,self.score))
    
    def feedback(self, feedback:Feedback) -> None:
        self.moves += feedback.moves
        self.turns += feedback.turns
        self.score += feedback.score
        print(feedback.as_string())
