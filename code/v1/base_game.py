from v1.tiles import *
from datetime import datetime

from v1.players import *
import pandas as pd
from v1.game_state import *


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


def setup_players(player_type_list, tiles, simulations):  # pragma: no cover
    players = []
    for i in range(4):
        if player_type_list[i] == "RANDOM":
            player = RandomAgent(tiles[i])
            players.append(player)
        elif player_type_list[i] == "MCTS":
            player = MCTSAgent(tiles[i], i, simulations)
            players.append(player)
        elif player_type_list[i] == "SEMIRANDOM":
            player = SemiRandomAgent(tiles[i])
            players.append(player)
    return players


def end_of_game_output(state, print_output):  # pragma: no cover
    discard = state._last_discarded
    if discard == DUMMY_TILE:
        if print_output:
            p = state._current_player_number
            print(f"Player {p} has won by pickup")
            state._players[p].all_tiles().print()
        else:
            p = float("NaN")
    elif state.any_wins(discard) != -1:
        p = state.any_wins(discard)
        state._players[p]._possible_discards.add(discard)
        if print_output:
            print(f"Player {p} has won from a discarded tile")
            state._players[p].all_tiles().print()
    else:
        p = float("NaN")
        if print_output:
            print("No winner")
    if print_output:
        print("GAME ENDED")
    return p


def main(player_types, completed_games, print_output=False):

    # initiate game state
    deck = create_tiles()
    player_tiles = distribute_tiles(deck)
    all_players = setup_players(player_types, player_tiles, completed_games)

    state = GameState(deck, all_players)

    # # print initial game state
    # state.print()

    # gameplay
    while not state.ended():
        state = state.next_game_state()
        for p in all_players:
            p.all_tiles().hand_score(p.unwanted_suit)

    # # end of game output
    # state.print()
    return end_of_game_output(state, print_output)


def review():
    startTime = datetime.now()
    agents = ["MCTS", "SEMIRANDOM", "SEMIRANDOM", "SEMIRANDOM"]
    main(agents, True)
    print(f"Game took {datetime.now() - startTime} to run.")


if __name__ == "__main__":
    main()
