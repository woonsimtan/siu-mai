from base_game import Tile, TileList


class RandomAgent:
    def __init__(self, distributed_tiles):
        self.pair = TileList()
        self.locked_tiles = TileList()
        self.possible_discards = distributed_tiles
        self.displayed_tiles = TileList()

    def play_a_turn(self, new_tile):
        if self.possible_discards.check_for_win():
            return "WIN"
        else:
            self.lock_triples()
            self.lock_pair()
            return self.discard()

    def discard(self):
        return possible_discards.remove_random_tile()

    def lock_three_of_a_kind(self):
        counts = self.possible_discards.tile_counts()
        triples = [tile for tile in counts.keys() if counts[tile] >= 3]
        for triple in triples:
            l = [triple for i in range(3)]
            self.locked_tiles.add_tiles(l)
            self.possible_discards.remove_tiles(l)
            
    def lock_three_consecutive(self):
        self.possible_discards.sort()
        for tile in self.possible_discards:
            second = Tile(tile.suit_type, str(int(tile.value) + 1))
            third = Tile(tile.suit_type, str(int(tile.value) + 2))
            if self.possible_discards.contains(second) and self.possible_discards.contains(third):
                self.possible_discards.remove_tiles(TileList([tile, second, third]))
                self.locked_tiles.add_tiles(TileList([tile, second, third]))

    def lock_triples(self):
        self.lock_three_of_a_kind()
        self.lock_three_consecutive()   

    def lock_pair(self):
        if self.pair.size() == 0:
            counts = self.possible_discards.tile_counts()
            pairs = [tile for tile in counts.keys() if counts[tile] >= 2]
            if len(pairs) > 0:
                pair_index = random.randint(0, len(pairs) - 1)
                pair_tile = pairs[pair_index]
                self.pair.add_tiles(TileList([pair_tile, pair_tile]))
                self.possible_discards.remove_tiles(TileList([pair_tile, pair_tile]))

