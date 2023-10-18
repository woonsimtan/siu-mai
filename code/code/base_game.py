# imports
import random
from collections import Counter
from abc import ABC, abstractmethod

# fixed values
SUIT_VALUES = {
    "Numbers": ["1", "2", "3", "4", "5", "6", "7", "8", "9"],
    "Circles": ["1", "2", "3", "4", "5", "6", "7", "8", "9"],
    "Bamboo": ["1", "2", "3", "4", "5", "6", "7", "8", "9"],
}

# Tile class definition
class Tile:
    def __init__(self, suit_type, value):
        self.suit_type = suit_type
        self.value = value

    def __eq__(self, other):
        return (self.suit_type == other.suit_type) and (self.value == other.value)

    def to_string(self):
        return self.suit_type + self.value

    def __lt__(self, other):
        if self.suit_type < other.suit_type:
            return True
        elif self.suit_type == other.suit_type and self.value < other.value:
            return True
        else:
            return False



class TileList:
    def __init__(self, tiles = []):
        self.tiles = tiles

    def sort(self):
        self.tiles = sorted(self.tiles, key=lambda x: (x.suit_type, x.value), reverse=False)

    def __eq__(self, other):
        self.sort()
        other.sort()
        return self.tiles == other.tiles

    def print_form(self):
        to_print = []
        # sort tiles
        self.sort()
        tile_list = self.tiles
        # print tiles
        for tile in tile_list:
            to_print.append(tile.to_string())
        return to_print

    def print(self):
        print(self.print_form())
        
    def add(self, new_tile):
        self.tiles.append(new_tile)

    def add_tiles(self, tile_list):
        for tile in tile_list.tiles:
            self.add(tile)

    def shuffle(self): # pragma: no cover
        random.shuffle(self.tiles)

    def remove(self, tile):
        if tile in self.tiles:
            self.tiles.remove(tile)
        else:
            raise ValueError("Tile to be removed is not in list.")

    def remove_tiles(self, tile_list):
        for tile in tile_list.tiles:
            self.remove(tile)
        
    def size(self):
        return len(self.tiles)

    def unique_tiles(self):
        tile_set = []
        for tile in self.tiles:
            if tile not in tile_set:
                tile_set.append(tile)
        return TileList(tile_set)

    def tile_counts(self):
        unique = self.unique_tiles().tiles
        counts = {}
        for tile in unique:
            counts[tile.to_string()] = self.count(tile)
        return counts

    def remove_random_tile(self):
        discard_index = random.randint(0, self.size() - 1)
        discarded_tile = self.tiles.pop(discard_index)
        return discarded_tile

    def contains(self, tile):
        return tile in self.tiles

    def check_for_peng(self, tile):
        return self.count(tile) == 2

    def count(self, tile):
        return self.tiles.count(tile)

    def copy(self):
        return TileList(self.tiles)

    def check_for_win(self, tile):
        copy = self.copy()
        copy.add(tile)
        copy.sort()

        takeout_pair = self.size() % 3 == 2
        if takeout_pair:
            counts = self.tile_counts()
            pairs = [tile for tile in counts.keys() if counts[tile] >= 2]
        else:
            pairs = ["dummy"]

        for pair in pairs:
            test = copy
            if takeout_pair:
                test.remove_tiles(TileList([pair, pair]))

            while test.size() > 0:
                t = test.tiles[0]
                if test.count(t) < 3:
                    t2 = Tile(t.suit_type, str(int(t.value) + 1))
                    t3 = Tile(t.suit_type, str(int(t.value) + 2))
                    if test.contains(t2) and test.contains(t3):
                        test.remove_tiles(TileList([t, t2, t3]))
                    else:
                        break
                elif test.count(t) < 3:
                    break
                else:
                    test.remove_tiles(TileList([t, t, t]))
            if test.size() == 0:
                return True
        return False



def create_tiles() -> TileList:
    all_tiles = TileList()
    # for every suit
    for key in SUIT_VALUES.keys():
        # for every value
        for value in SUIT_VALUES[key]:
            # create 4 tiles
            all_tiles.add_tiles(TileList([Tile(key, value) for i in range(4)]))
    # shuffle
    all_tiles.shuffle()
    # return list of tiles
    return all_tiles

# def distribute_tiles(to_distribute):
#     player_tiles = [TileList(), TileList(), TileList(), TileList()]
#     player_tiles[0].print()
#     for i in range(13):
#         for j in range(4):
#             t = to_distribute.remove_random_tile()
#             print(t.to_string())
#             player_tiles[j].add(t)
#     return player_tiles




def main():
    player_types = ["RANDOM", "RANDOM", "RANDOM", "RANDOM"]
    deck = create_tiles()
    deck.print()
    # distributed = distribute_tiles(deck)

    print(deck.size())
    # print(distributed[0].size())





