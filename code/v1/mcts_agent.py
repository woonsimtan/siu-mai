from v1.tiles import *
from v1.mcts_node import *


class MCTSAgent:
    def __init__(self, distributed_tiles, player_number):
        self.possible_discards = distributed_tiles
        self.displayed_tiles = TileList([])
        self.player_number = player_number

    def get_possible_discards(self):
        return self.possible_discards

    def print_all_tiles(self):
        self.all_tiles().print()

    def get_hidden_tiles(self):
        return self.possible_discards

    def all_tiles(self):
        combined = self.possible_discards.copy()
        combined.add_tiles(self.displayed_tiles)
        return combined

    def pickup(self, tile):
        self.possible_discards.add(tile)

    def get_game_state(self, players, discarded_tiles, deck, last_discarded):
        all_seen = discarded_tiles.copy()
        for p in players:
            all_seen.add_tiles(p.displayed_tiles)

        state = GameState(
            players,
            all_seen,
            deck,
            last_discarded,
            self.player_number,
            self.player_number,
        )
        #     state = {
        #         "player_tiles": players,
        #         "displayed_tiles": all_seen,
        #         "hidden_tiles": deck.copy(),
        #         "discarded_tile": last_discarded,
        #         "current_player": self.player_number,
        #         "maximising_player": self.player_number,
        #     }
        return state

    def discard(self, players, discarded_tiles, deck, last_discarded):
        initial_state = self.get_game_state(
            players, discarded_tiles, deck, last_discarded
        )
        root = MonteCarloTreeSearchNode(state=initial_state, parent_action="PICKUP")
        selected_node = root.best_action()
        tile = selected_node.parent_action[1]
        return tile
        # TBC

    def peng(self, tile):
        # print(tile.to_string())
        # self.possible_discards.print()
        self.possible_discards.add(tile)
        l = TileList([tile for i in range(3)])
        self.displayed_tiles.add_tiles(l)
        self.possible_discards.remove_tiles(l)

    def choose_peng(self):
        # TBD
        return True

    def check_for_win(self, tile=None):
        return self.all_tiles().check_for_win(tile)

    def check_for_peng(self, tile=None):
        return self.get_hidden_tiles().check_for_peng(tile)
