from v1.tiles import *

# from v1.random_agent import *
from v1.players import *
import pandas as pd
from v1.game_state import *

# from v1.mcts_agent import *

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


def setup_players(player_type_list, tiles):  # pragma: no cover
    players = []
    for i in range(4):
        if player_type_list[i] == "RANDOM":
            player = RandomAgent(tiles[i])
            players.append(player)
        elif player_type_list[i] == "MCTS":
            player = MCTSAgent(tiles[i])
            players.append(player)
        elif player_type_list[i] == "SEMIRANDOM":
            player = SemiRandomAgent(tiles[i])
            players.append(player)
    return players


# def end_of_game_output(hands, discard, player):  # pragma: no cover
#     if discard == DUMMY_TILE:
#         # pass
#         print(f"Player {player} has won by pickup")
#         hands[player].all_tiles().print()
#     elif any_wins(hands, discard) != -1:
#         player = any_wins(hands, discard)
#         hands[player]._possible_discards.add(discard)
#         print(f"Player {player} has won from a discarded tile")
#         hands[player].all_tiles().print()
#     else:
#         player = float("NaN")
#         print("No winner")
#     print("GAME ENDED")
#     return player


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


def main(player_types, print_output=False):
    # initiate game state

    deck = create_tiles()
    player_tiles = distribute_tiles(deck)
    all_players = setup_players(player_types, player_tiles)

    state = GameState(deck, all_players)

    # print initial game state
    # state.print()

    # gameplay
    while not state.ended():
        action = state.get_next_action()
        state = state.update_game_state(action)

        # state.print()

    # end of game output
    return end_of_game_output(state, print_output)


# def main(player_types):  # pragma: no cover
#     # set initial values

#     player_number = 0
#     discarded_tiles = TileList([])
#     last_discarded = DUMMY_TILE
#     turn = 1

#     deck = create_tiles()
#     player_tiles = distribute_tiles(deck)
#     all_players = setup_players(player_types, player_tiles)

#     # gameplay
#     while any_wins(all_players, last_discarded) == -1 and deck.size() > 0:
#         # check for players that can peng
#         can_peng = any_peng((player_number + 3) % 4, all_players, last_discarded) != -1
#         chose_peng = False
#         # if can peng
#         if can_peng:
#             peng_player = any_peng((player_number + 3) % 4, all_players, last_discarded)
#             player = all_players[peng_player]
#             chose_peng = player.choose_peng()
#             if chose_peng:
#                 player_number = peng_player
#                 player.peng(last_discarded)

#         # pickup
#         if not can_peng or not chose_peng:
#             discarded_tiles.add(last_discarded)
#             player = all_players[player_number]
#             new_tile = deck.remove_random_tile()
#             if player.check_for_win(new_tile):
#                 break
#             else:
#                 player.pickup(new_tile)

#         # discard
#         last_discarded = all_players[player_number].discard()

#         turn += 1

#         # if anyone has won from pickup
#         if last_discarded == DUMMY_TILE:
#             break

#         # next player
#         player_number = (player_number + 1) % 4

#     # end of game output
#     return end_of_game_output(all_players, last_discarded, player_number)


def review():
    agents = ["SEMIRANDOM", "SEMIRANDOM", "SEMIRANDOM", "SEMIRANDOM"]
    main(agents, True)
