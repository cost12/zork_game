import sys

from utils.visualize_game   import visualize_game
from controls.game_control  import GameState
from models.actors          import Actor
from readin.level1_readin   import get_level1
from logging_config         import setup_logging

setup_logging()

def main(args:list[str]):
    if len(args) > 0:
        if args[0] in ['visualize','v','vis']:
            visualize_game(args[1])
            return
    world, name_space, controllers, details = get_level1()
    players = 1
    while 0 and (players < details['min_players'] or players > details['max_players']):
        players = int(input("How many players are playing? "))

    extra_characters = list[Actor]()
    if players > details['playable_characters']:
        pass
    if players < details['playable_characters']:
        pass

    game = GameState(details, world, name_space, extra_characters, controllers)
    game.play()

if __name__=="__main__":
    main(sys.argv[1:])
