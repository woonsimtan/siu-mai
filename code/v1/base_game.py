from v1.tiles import *
from v1.random_agent import *

# fixed values
SUIT_VALUES = {
    "Numbers": ["1", "2", "3", "4", "5", "6", "7", "8", "9"],
    "Circles": ["1", "2", "3", "4", "5", "6", "7", "8", "9"],
    "Bamboo": ["1", "2", "3", "4", "5", "6", "7", "8", "9"],
}


def create_tiles(tiles=SUIT_VALUES) -> TileList:
    all_tiles = TileList()
    # for every suit
    for key in tiles.keys():
        # for every value
        for value in tiles[key]:
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
        raise ValueError(
            f"Player {i} has invalid number of tiles: {p.possible_discards.size()}"
        )


def setup_players(player_type_list, tiles): # pragma: no cover
    players = []
    for i in range(4):
        if player_type_list[i] == "RANDOM":
            player = RandomAgent(tiles[i])
            players.append(player)
    return players


def main(): # pragma: no cover
    # set initial values
    player_types = ["RANDOM", "RANDOM", "RANDOM", "RANDOM"]
    player_number = 0
    discarded_tiles = TileList()
    last_discarded = DUMMY_TILE

    deck = create_tiles()
    player_tiles = distribute_tiles(deck)
    all_players = setup_players(player_types, player_tiles)

    # gameplay
    while any_wins(all_players, last_discarded) == -1 and deck.size() > 0:
        # check for players that can peng - assume peng if they can
        peng = any_peng(all_players, last_discarded)
        if peng != -1:
            player_number = peng
            player = all_players[player_number]
            last_discarded = all_players[player_number].peng(last_discarded)
        else:
            player = all_players[player_number]
            pickup = deck.remove_random_tile()
            last_discarded = all_players[player_number].play_a_turn(pickup)

        # if anyone has won from pickup
        if last_discarded == DUMMY_TILE:
            break

        # next player
        player_number = (player_number + 1) % 4

    # end of game output
    if last_discarded == DUMMY_TILE:
        print(f"Player {player_number} has won by pickup")
        all_players[player_number].print_all_tiles()
    elif any_wins(all_players, last_discarded) != -1:
        player_number = any_wins(all_players, last_discarded)
        all_players[player_number].possible_discards.add(last_discarded)
        print(f"Player {player_number} has won from a discarded tile")

        all_players[player_number].print_all_tiles()
    else:
        print("Nobody won")
    print("GAME ENDED")
