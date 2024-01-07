from v1.tiles import *
from v1.random_agent import *
import pandas as pd
from v1.mcts_agent import *

# fixed values
SUIT_VALUES = {
    "Numbers": ["1", "2", "3", "4", "5", "6", "7", "8", "9"],
    "Circles": ["1", "2", "3", "4", "5", "6", "7", "8", "9"],
    "Bamboo": ["1", "2", "3", "4", "5", "6", "7", "8", "9"],
}


def create_tiles(tiles=SUIT_VALUES) -> TileList:
    all_tiles = TileList([])
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
        p.print_all_tiles()
        raise ValueError(
            f"Player {i} has invalid number of tiles: {p.all_tiles().size()}"
        )


def setup_players(player_type_list, tiles):  # pragma: no cover
    players = []
    for i in range(4):
        if player_type_list[i] == "RANDOM":
            player = RandomAgent(tiles[i])
            players.append(player)
        elif player_type_list[i] == "MCTS":
            player = MCTSAgent(tiles[i], i)
            players.append(player)
        elif player_type_list[i] == "SEMIRANDOM":
            player = SemiRandomAgent(tiles[i])
            players.append(player)
    return players


def end_of_game_output(hands, discard, player):
    if discard == DUMMY_TILE:
        pass
        # print(f"Player {player} has won by pickup")
        # hands[player].print_all_tiles()
    elif any_wins(hands, discard) != -1:
        player = any_wins(hands, discard)
        hands[player].possible_discards.add(discard)
        # print(f"Player {player} has won from a discarded tile")
        # hands[player].print_all_tiles()
    else:
        player = float("NaN")
        # print("No winner")
    # print("GAME ENDED")
    return player


def main(player_types):  # pragma: no cover
    # set initial values

    player_number = 0
    discarded_tiles = TileList([])
    last_discarded = DUMMY_TILE
    turn = 1

    deck = create_tiles()
    player_tiles = distribute_tiles(deck)
    all_players = setup_players(player_types, player_tiles)

    # gameplay
    while any_wins(all_players, last_discarded) == -1 and deck.size() > 0:
        # check for players that can peng
        peng = any_peng(all_players, last_discarded)
        # if can peng
        if peng != -1:
            player = all_players[peng]
            chose_peng = player.choose_peng()
            if chose_peng:
                player_number = peng
                player.peng(last_discarded)

        # pickup
        if peng == -1 or not chose_peng:
            discarded_tiles.add(last_discarded)
            player = all_players[player_number]
            new_tile = deck.remove_random_tile()
            if player.check_for_win(new_tile):
                break
            else:
                player.pickup(new_tile)

        # discard
        last_discarded = all_players[player_number].discard(
            all_players, discarded_tiles, deck, last_discarded
        )

        turn += 1

        # if anyone has won from pickup
        if last_discarded == DUMMY_TILE:
            break

        # print(f"Player {player_number} has finished a turn.")

        # next player
        player_number = (player_number + 1) % 4

    # end of game output
    return end_of_game_output(all_players, last_discarded, player_number)
