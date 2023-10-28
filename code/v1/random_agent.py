from v1.tiles import *


class RandomAgent:
    def __init__(self, distributed_tiles):
        self.pair = TileList([])
        self.locked_tiles = TileList([])
        self.possible_discards = distributed_tiles
        self.displayed_tiles = TileList([])

    def all_tiles(self):
        combined = TileList([])
        combined.add_tiles(self.pair)
        combined.add_tiles(self.locked_tiles)
        combined.add_tiles(self.possible_discards)
        combined.add_tiles(self.displayed_tiles)
        return combined

    def print_all_tiles(self):  # pragma: no cover
        self.all_tiles().print()

    def total_tile_count(self):
        # TODO: raise error if more than 14 tiles
        return (
            self.pair.size()
            + self.locked_tiles.size()
            + self.possible_discards.size()
            + self.displayed_tiles.size()
        )

    def play_a_turn(self, new_tile):
        win = self.possible_discards.check_for_win(new_tile)
        self.possible_discards.add(new_tile)
        if win:
            return DUMMY_TILE
        else:
            self.lock_triples()
            self.lock_pair()
            return self.discard()

    def discard(self):
        return self.possible_discards.remove_random_tile()

    def lock_three_of_a_kind(self):
        counts = self.possible_discards.tile_counts()
        triples = [
            Tile(tile_str[:-1], tile_str[-1])
            for tile_str in counts.keys()
            if counts[tile_str] >= 3
        ]
        for triple in triples:
            l = TileList([triple for i in range(3)])
            self.locked_tiles.add_tiles(l)
            self.possible_discards.remove_tiles(l)

    def lock_three_consecutive(self):
        self.possible_discards.sort()
        for tile in self.possible_discards.tiles:
            second = Tile(tile.suit_type, str(int(tile.value) + 1))
            third = Tile(tile.suit_type, str(int(tile.value) + 2))
            if self.possible_discards.contains(
                second
            ) and self.possible_discards.contains(third):
                self.possible_discards.remove_tiles(TileList([tile, second, third]))
                self.locked_tiles.add_tiles(TileList([tile, second, third]))

    def lock_triples(self):
        self.lock_three_of_a_kind()
        self.lock_three_consecutive()

    def lock_pair(self):
        if self.pair.size() == 0:
            counts = self.possible_discards.tile_counts()
            pairs = [
                Tile(tile_str[:-1], tile_str[-1])
                for tile_str in counts.keys()
                if counts[tile_str] >= 2
            ]
            if len(pairs) > 0:
                pair_index = random.randint(0, len(pairs) - 1)
                pair_tile = pairs[pair_index]
                self.pair.add_tiles(TileList([pair_tile, pair_tile]))
                self.possible_discards.remove_tiles(TileList([pair_tile, pair_tile]))

    def check_for_win(self, tile):
        all_tiles = self.all_tiles()
        return all_tiles.check_for_win(tile)

    def check_for_peng(self, tile):
        return self.possible_discards.check_for_peng(tile)

    def peng(self, tile):
        self.possible_discards.add(tile)
        l = TileList([tile for i in range(3)])
        self.displayed_tiles.add_tiles(l)
        self.possible_discards.remove_tiles(l)
        return self.discard()
