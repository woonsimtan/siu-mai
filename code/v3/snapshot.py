from v3.base_game import *
from v3.players import MCTSAgent as MCTSAgentV2
from v3.tiles import *
from v3.game_state import *

# Example 1: Human would discard Numbers9
tile_str = [
    "Circles1",
    "Circles1",
    "Circles1",
    "Bamboo3",
    "Bamboo3",
    "Bamboo3",
    "Circles3",
    "Circles3",
    "Circles9",
    "Circles8",
    "Circles6",
    "Bamboo6",
    "Bamboo7",
    "Bamboo1",
]
input_tile_list = TileList([Tile(tile[:-1], tile[-1]) for tile in tile_str])

deck = create_tiles()
deck.remove_tiles(input_tile_list)
deck.shuffle()

players = setup_players(
    ["SEMIRANDOM", "SEMIRANDOM", "SEMIRANDOM", "SEMIRANDOM"],
    distribute_tiles(deck),
    100,
)
deck.add_tiles(players[0].all_tiles())
players[0] = MCTSAgentV2(input_tile_list, 0, 1000)
game_state = GameState(
    deck, players, current_player_number=0, last_discarded=DUMMY_TILE
)

input_tile_list.print()
print("")
print("Human: ", "Circles9")

R1 = RandomAgent(input_tile_list)
print("Random: ", R1.discard().to_string())

S1 = SemiRandomAgent(input_tile_list)
print("Semi-Random: ", S1.discard().to_string())

H1 = HandScoreAgent(input_tile_list)
print("Hand Score: ", H1.discard().to_string())

# MC1 = MCTSAgent(input_tile_list, 0, 100)
# print("MCTS V1: ", MC1.discard().to_string())

# MC2 = MCTSAgentV2(input_tile_list, 0, 100)
print("MCTS V2: ", players[0].discard(game_state).to_string())
