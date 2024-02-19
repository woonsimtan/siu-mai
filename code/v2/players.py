from abc import ABC, abstractmethod
import random
from tiles import *
from mcts import MonteCarloTreeSearchNode


class Player(ABC):
    def __init__(
        self, possible_discards, displayed_tiles=TileList([]), unwanted_suit=None
    ):
        self._displayed_tiles = displayed_tiles
        self._possible_discards = possible_discards

        if unwanted_suit is None:

            tiles_by_suit = self.possible_discards.get_tiles_by_suit()
            unwanted = list(tiles_by_suit.keys())[0]
            for suit in tiles_by_suit.keys():
                if tiles_by_suit[suit].size() < tiles_by_suit[unwanted].size():
                    unwanted = suit
                elif tiles_by_suit[suit].size() == tiles_by_suit[unwanted].size():
                    unwanted = random.choice([suit, unwanted])
            self.unwanted_suit = unwanted
        else:
            self.unwanted_suit = unwanted_suit

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
        if tiles_by_suit[self.unwanted_suit].size() == 0:
            try:
                return self._possible_discards.remove_random_tile()
            except:
                print(self.unwanted_suit)
                self._displayed_tiles.print()
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

    def win_score(self, deck_empty, tile=None):
        # should this be taking discarded tile

        hand = self.all_tiles()

        # doesn't need unwanted suit because needs to have won before calculating win score

        # basic fan = 0 -> 1 point for winning
        fan = 0

        # root (using 4 identical tiles) - 1 fan for each set
        counts = hand.tile_counts()
        for c in counts.values():
            if c >= 4:
                fan += 1

        # all pengs (4 sets of pengs) - 1 fan
        pengs = 0
        pairs = 0
        for c in counts.values():
            if c == 3:
                pengs += 1
            elif c == 2:
                pairs += 1

        if pengs == 4 or (pengs == 3 and pairs == 2):
            fan += 1
        
        # golden single wait (4 sets of declared pengs and waiting for a pair) - 1 fan
        displayed_counts = self.displayed_tiles.tile_counts()
        displayed_pengs = 0
        for c in displayed_counts.values():
            if c == 3:
                displayed_pengs += 1
        if displayed_pengs == 4:
            fan += 1

        # full flush (all tiles from 1 suit) - 2 fan
        suits = hand.get_tiles_by_suit()
        for suit in suits.values():
            if suit.size() == 14 or suit.size() == 13:
                fan += 2

        # 7 pairs - 2 fan
        copy = hand.copy()
        if tile is not None and tile != DUMMY_TILE:
            copy.add(tile)

        counts = copy.tile_counts()
        pairs = 0
        for c in counts.values():
            if c == 2:
                pairs += 1
            elif c == 4:
                pairs += 2
        if pairs == 7:
            fan += 2

        # under the sea (winning by self draw on last tile or by discard after the last tile) - 1 fan
        if deck_empty:
            fan += 1

        # self draw - 1 fan
        if hand.size() == 14:
            fan += 1

        # 3 fan is max 
        # (but maybe should remove this? larger scores might give mcts better results)
        if fan > 3:
            fan = 3

        return 2 ** fan


class RandomAgent(Player):
    pass


class SemiRandomAgent(Player):
    def __init__(
        self, possible_discards, displayed_tiles=TileList([]), unwanted_suit=None
    ):
        super().__init__(possible_discards, displayed_tiles, unwanted_suit)
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
                    self._possible_discards.remove_tiles(
                        TileList([tile, second, third])
                    )
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
        if tiles_by_suit[self.unwanted_suit].size() > 0:
            tile = tiles_by_suit[self.unwanted_suit].remove_random_tile()
            self._possible_discards.remove(tile)
            return tile
        else:
            # create state for mcts
            # print("initialised with current player: ", game_state._current_player_number)
            root = MonteCarloTreeSearchNode(
                game_state.initialise_mcts_state(), self.simulations_to_run
            )
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
