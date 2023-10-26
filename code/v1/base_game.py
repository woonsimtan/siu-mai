from v1.tiles import *
from v1.random_agent import *

# fixed values
SUIT_VALUES = {
    "Numbers": ["1", "2", "3", "4", "5", "6", "7", "8", "9"],
    "Circles": ["1", "2", "3", "4", "5", "6", "7", "8", "9"],
    "Bamboo": ["1", "2", "3", "4", "5", "6", "7", "8", "9"],
}


def create_tiles() -> TileList:
    all_tiles = TileList()
    # for every suit
    for key in SUIT_VALUES.keys():
        # for every value
        for value in SUIT_VALUES[key]:
            # create 4 tiles
            all_tiles.add_tiles(TileList([Tile(key, value) for i in range(4)]))
    # shuffle
    all_tiles.shuffle()
    # return list of tiles
    return all_tiles

def distribute_tiles(to_distribute):
    player_tiles = [[], [], [], []]
    for i in range(13):
        for j in range(4):
            t = to_distribute.remove_random_tile()
            player_tiles[j].append(t)
    return [TileList(tiles) for tiles in player_tiles]


def any_peng(players, discarded):
    for i in range(4):
        p = players[i]
        if p.check_for_peng(discarded):
            return i
    return -1

def any_wins(players, discarded):
    try:
        for i in range(4):
            p = players[i]
            if p.check_for_win(discarded):
                return i
        return -1
    except ValueError:
        raise ValueError(f"Player {i} has invalid number of tiles: {p.possible_discards.size()}")

def setup_players(player_type_list, tiles):
    players = []
    for i in range(4):
        if player_type_list[i] == "RANDOM":
            player = RandomAgent(tiles[i])
            players.append(player)
    return players

def print_game_output(player, number, pickup, last_discarded):
    print("---------------")
    print(player.displayed_tiles.size() + player.possible_discards.size() + player.locked_tiles.size() + player.pair.size())

    print (f"Player {number} picked up: {pickup.to_string()}")
    player.possible_discards.print()
    player.displayed_tiles.print()
    player.locked_tiles.print()
    player.pair.print()
    print (f"Player {number} discarded: {last_discarded.to_string()}")



def main():
    # set initial values
    player_types = ["RANDOM", "RANDOM", "RANDOM", "RANDOM"]
    player_number = 0
    discarded_tiles = TileList()
    last_discarded = Tile("DUMMY", "TILE")

    deck = create_tiles()
    player_tiles = distribute_tiles(deck)
    all_players = setup_players(player_types, player_tiles)

    for player in all_players:
        print(player.displayed_tiles.size() + player.possible_discards.size() + player.locked_tiles.size() + player.pair.size())


# current bug is that tile count of player goes over 14?
    while any_wins(all_players, last_discarded) == -1 and deck.size() > 0:

        # if someone can peng
        if any_peng(all_players, last_discarded) != -1:
            player_number = any_peng(all_players, last_discarded)
            player = all_players[player_number]
            # print(player.displayed_tiles.size() + player.possible_discards.size() + player.locked_tiles.size() + player.pair.size())

            last_discarded = all_players[player_number].peng(last_discarded)
            # print(player.displayed_tiles.size() + player.possible_discards.size() + player.locked_tiles.size() + player.pair.size())


        else:
            player = all_players[player_number]
            # print(player.displayed_tiles.size() + player.possible_discards.size() + player.locked_tiles.size() + player.pair.size())

            pickup = deck.remove_random_tile()
            last_discarded = all_players[player_number].play_a_turn(pickup)
            # print_game_output(all_players[player_number], player_number, pickup, last_discarded)

        print(player_number)
        print(player.displayed_tiles.size() + player.possible_discards.size() + player.locked_tiles.size() + player.pair.size())
        
            
            
        # if anyone has won end the game
        if isinstance(last_discarded, str):
            break
            
        player_number = (player_number + 1) % 4

    print("GAME ENDED")







    





