from abc import ABC, abstractmethod
import random
from tiles import *
from mcts import MonteCarloTreeSearchNode


class Player(ABC):
    def __init__(self, possible_discards, displayed_tiles=TileList([])):
        self._displayed_tiles = displayed_tiles
        self._possible_discards = possible_discards
        
        tiles_by_suit = self.possible_discards.get_tiles_by_suit()
        unwanted = list(tiles_by_suit.keys())[0]
        for suit in tiles_by_suit.keys():
            if tiles_by_suit[suit].size() < tiles_by_suit[unwanted].size():
                unwanted = suit

        self.unwanted_suit = unwanted

    @property
    def displayed_tiles(self):
        return self._displayed_tiles.copy()

    @displayed_tiles.setter
    def displayed_tiles(self, value):
        self._displayed_tiles = value

    @property
    def possible_discards(self):
        return self._possible_discards.copy()

    @possible_discards.setter
    def possible_discards(self, value):
        self._possible_discards = value

    def pickup(self, tile):
        self._possible_discards.add(tile)

    def all_tiles(self):
        complete_hand = self.possible_discards
        complete_hand.add_tiles(self.displayed_tiles)
        return complete_hand

    def check_for_win(self, tile=None):
        all_tiles = self.all_tiles()
        for t in all_tiles.tiles:
            if t.suit_type == self.unwanted_suit:
                return False
        return all_tiles.check_for_win(tile)

    def check_for_peng(self, tile):
        if tile.suit_type != self.unwanted_suit:
            return self._possible_discards.check_for_peng(tile)
        else:
            return False

    def choose_peng(self):
        return True

    def peng(self, tile):
        self._possible_discards.add(tile)
        l = TileList([tile] * 3)
        self._displayed_tiles.add_tiles(l)
        self._possible_discards.remove_tiles(l)

    def discard(self, game_state=None):
        tiles_by_suit = self.possible_discards.get_tiles_by_suit()
        if self.unwanted_suit not in tiles_by_suit.keys():
            try:
                return self._possible_discards.remove_random_tile()
            except:
                self._possible_discards.print()
                self.all_tiles().print()
                raise ValueError("Random discard failed")
        else:
            tile = tiles_by_suit[self.unwanted_suit].remove_random_tile()
            self._possible_discards.remove(tile)
            return tile

    def get_hidden_tiles(self):
        return self.possible_discards

    def total_tile_count(self):
        return self.all_tiles().size()

    def is_mcts(self):
        return False


class RandomAgent(Player):
    pass


class SemiRandomAgent(Player):
    def __init__(self, possible_discards, displayed_tiles=TileList([])):
        super().__init__(possible_discards, displayed_tiles)
        self._pair = TileList([])
        self._locked_tiles = TileList([])

    @property
    def pair(self):
        return self._pair.copy()

    @property
    def locked_tiles(self):
        return self._locked_tiles.copy()

    def all_tiles(self):
        combined = self.get_hidden_tiles()
        combined.add_tiles(self.displayed_tiles)
        return combined

    def get_hidden_tiles(self):
        hidden = TileList([])
        hidden.add_tiles(self.pair)
        hidden.add_tiles(self.locked_tiles)
        hidden.add_tiles(self.possible_discards)
        return hidden

    def pickup(self, tile):
        self._possible_discards.add(tile)
        self.lock_triples()
        self.lock_pair()

    def lock_three_of_a_kind(self):
        counts = self.possible_discards.tile_counts()
        triples = [
            Tile(tile_str[:-1], tile_str[-1])
            for tile_str in counts.keys()
            if counts[tile_str] >= 3 and tile_str[:-1] != self.unwanted_suit
        ]
        for triple in triples:
            l = TileList([triple for i in range(3)])
            self._locked_tiles.add_tiles(l)
            self._possible_discards.remove_tiles(l)

    def lock_three_consecutive(self):
        self._possible_discards.sort()
        for tile in self.possible_discards.tiles:
            if tile.suit_type != self.unwanted_suit:
                second = Tile(tile.suit_type, str(int(tile.value) + 1))
                third = Tile(tile.suit_type, str(int(tile.value) + 2))
                if (
                    self.possible_discards.contains(tile)
                    and self.possible_discards.contains(second)
                    and self.possible_discards.contains(third)
                ):
                    self._possible_discards.remove_tiles(TileList([tile, second, third]))
                    self._locked_tiles.add_tiles(TileList([tile, second, third]))

    def lock_triples(self):
        self.lock_three_of_a_kind()
        self.lock_three_consecutive()

    def lock_pair(self):
        if self.pair.size() == 0:
            counts = self.possible_discards.tile_counts()
            pairs = [
                Tile(tile_str[:-1], tile_str[-1])
                for tile_str in counts.keys()
                if counts[tile_str] >= 2 and tile_str[:-1] != self.unwanted_suit
            ]
            if len(pairs) > 0:
                pair_index = random.randint(0, len(pairs) - 1)
                pair_tile = pairs[pair_index]
                self._pair.add_tiles(TileList([pair_tile, pair_tile]))
                self._possible_discards.remove_tiles(TileList([pair_tile, pair_tile]))


class MCTSAgent(Player):
    def __init__(self, possible_discards, player_number, simulations):
        super().__init__(possible_discards)
        self.player_number = player_number
        self.simulations_to_run = simulations

    def discard(self, game_state):

        tiles_by_suit = self.possible_discards.get_tiles_by_suit()
        if self.unwanted_suit in tiles_by_suit.keys():
            tile = tiles_by_suit[self.unwanted_suit].remove_random_tile()
            self._possible_discards.remove(tile)
            return tile
        else:
            # create state for mcts
            # print("initialised with current player: ", game_state._current_player_number)
            root = MonteCarloTreeSearchNode(game_state.initialise_mcts_state(), self.simulations_to_run)
            selected_node = root.best_action()

            if selected_node == -1:
                # print("MCTS failed: discarding random tile")
                return self._possible_discards.remove_random_tile()
            else:
                # print(
                #     "action selected: discard", selected_node.parent_action[1].to_string()
                # )
                self._possible_discards.remove_tiles(
                    TileList([selected_node.parent_action[1]])
                )
                return selected_node.parent_action[1]

    def is_mcts(self):
        return True
