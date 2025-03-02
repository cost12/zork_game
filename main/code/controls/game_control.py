from code.controls.input_handler import translate
from code.controls.character_control import GameState
from code.controls.character_control import CharacterController
import code.views.string_views as views

def game_control(game_state:GameState) -> None:

    while not game_state.game_over():
        controller = game_state.whose_turn().get_controller()
        user_input = controller.make_move()
        action, inputs = translate(user_input)
        feedback = game_state.action(game_state.whose_turn(), action, inputs)
        controller.feedback(feedback)