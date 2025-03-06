from code.controls.character_control import GameState
from code.models.data_read_in import read_in_game
from code.models.character import Character

def main():
    #game_name = input("Which game do you want to play? ")
    game_name = 'game0'
    game_rooms, game_characters, actions, items, directions, details = read_in_game(game_name)
    players = 1
    while 0 and (players < details['min_players'] or players > details['max_players']):
        players = int(input("How many players are playing? "))
    
    extra_characters = list[Character]()
    if players > details['playable_characters']:
        for i in range(players-details['playable_characters']):
            name = input(f"Name player {i}: ")
            extra_characters.append(Character(name, 'human'))
    if players < details['playable_characters']:
        pass
    
    game = GameState(game_rooms, game_characters, extra_characters, actions, items, directions)
    game.play()

if __name__=="__main__":
    main()