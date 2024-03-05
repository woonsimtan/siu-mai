from tiles import *
from datetime import datetime

from players import *
from game_state import *

from typing import List, Tuple


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


def distribute_tiles(to_distribute: TileList) -> List[TileList]:
    player_tiles = [[], [], [], []]
    for i in range(13):
        for j in range(4):
            t = to_distribute.remove_random_tile()
            player_tiles[j].append(t)
    return [TileList(tiles) for tiles in player_tiles]


def setup_players(player_type_list: List[str], tiles: List[TileList], simulations: int) -> List[Player]:
    players = []
    for i in range(4):
        if player_type_list[i] == "RANDOM":
            player = RandomAgent(tiles[i])
        elif player_type_list[i] == "MCTS":
            player = MCTSAgent(tiles[i], i, simulations)
        elif player_type_list[i] == "SEMIRANDOM":
            player = SemiRandomAgent(tiles[i])
        elif player_type_list[i] == "HANDSCORE":
            player = HandScoreAgent(tiles[i])
        players.append(player)
    return players


def end_of_game_output(state: GameState, print_output: bool) -> Tuple[List[int], List[int]]:  # pragma: no cover
    scores = [player.score for player in state._players]
    wins = [player.times_won for player in state._players]

    if print_output:
        print("GAME ENDED")
        for i in range(4):
            print(f"Player {i} score: {state._players[i].score}")

    return scores + wins


def main(player_types: List[str], simulations: int, print_output: bool = False):

    # initiate game state
    deck = create_tiles()
    player_tiles = distribute_tiles(deck)
    all_players = setup_players(player_types, player_tiles, simulations)

    state = GameState(deck, all_players)

    # gameplay
    while not state.ended():
        state = state.next_game_state()

    return end_of_game_output(state, print_output)


def review() -> None:
    startTime = datetime.now()
    agents = ["MCTS", "SEMIRANDOM", "SEMIRANDOM", "SEMIRANDOM"]
    main(agents, True)
    print(f"Game took {datetime.now() - startTime} to run.")


if __name__ == "__main__":
    main()
