import sys

from utils.visualize_game import visualize_game
from controls.game_control import GameState
from factories.data_read_in import read_in_game
from models.actors import Actor

def main(args:list[str]):
    if len(args) > 0:
        if args[0] in ['visualize','v','vis']:
            visualize_game(args[1])
            return
    #game_name = input("Which game do you want to play? ")
    game_name = 'game0'
    rooms, characters, controllers, items, actions, directions, details = read_in_game(game_name)
    players = 1
    while 0 and (players < details['min_players'] or players > details['max_players']):
        players = int(input("How many players are playing? "))
    
    extra_characters = list[Actor]()
    if players > details['playable_characters']:
        pass
    if players < details['playable_characters']:
        pass
    
    game = GameState(details, rooms, characters, extra_characters, controllers, actions, items, directions)
    game.play()

if __name__=="__main__":
    main(sys.argv[1:])