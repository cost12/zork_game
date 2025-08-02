from typing                     import Optional

from models.actors              import Actor
from controls.character_control import CharacterController, CommandLineController

class CharacterControlFactory:

    def __init__(self):
        self.characters = dict[Actor,CharacterController]()

    def create_character(self, character:Actor, controller:CharacterController) -> None:
        self.characters[character] = controller

    def get_controller(self, character:Actor) -> Optional[CharacterController]:
        return self.characters.get(character, None)

    def playable_characters(self) -> int:
        return len([1 for _,control in self.characters.items() if isinstance(control, CommandLineController)])
