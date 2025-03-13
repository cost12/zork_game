from controls.game_control import GameState
from factories.data_read_in import read_in_game
from models.character import Character

def main():
    #game_name = input("Which game do you want to play? ")
    game_name = 'game0'
    rooms, characters, controllers, items, actions, directions, details = read_in_game(game_name)
    players = 1
    while 0 and (players < details['min_players'] or players > details['max_players']):
        players = int(input("How many players are playing? "))
    
    extra_characters = list[Character]()
    if players > details['playable_characters']:
        pass
    if players < details['playable_characters']:
        pass
    
    game = GameState(details, rooms, characters, extra_characters, controllers, actions, items, directions)
    game.play()

if __name__=="__main__":
    main()