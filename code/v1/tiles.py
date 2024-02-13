# imports
import random
from collections import Counter
from abc import ABC, abstractmethod



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

    def print(self):
        print(self.to_string())

    def copy(self):
        return Tile(self.suit_type, self.value)


DUMMY_TILE = Tile("DUMMY", "TILE")


class TileList:
    def __init__(self, tiles=[]):
        self.tiles = tiles

    def sort(self):
        self.tiles = sorted(
            self.tiles, key=lambda x: (x.suit_type, x.value), reverse=False
        )

    def __eq__(self, other):
        self.sort()
        other.sort()
        return self.tiles == other.tiles
    
    def get_tiles_by_suit(self):
        tiles_by_suit = {}
        for t in self.tiles:
            if t.suit_type not in tiles_by_suit.keys():
                tiles_by_suit[t.suit_type] = TileList([t])
            else:
                tiles_by_suit[t.suit_type].add(t)
        return tiles_by_suit


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

    def shuffle(self):  # pragma: no cover
        random.shuffle(self.tiles)

    def remove(self, tile):
        if tile in self.tiles:
            self.tiles.remove(tile)
        else:
            self.print()
            raise ValueError(f"Tile to be removed is not in list: {tile.to_string()}")

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
        x = 0
        for t in self.tiles:
            if tile == t:
                x += 1
        return x

    def copy(self):
        tiles = self.tiles.copy()
        return TileList(tiles)

    def check_for_win(self, tile=None):
        copy = self.copy()
        if tile is not None:
            if copy.size() == 13:
                copy.add(tile)

        while DUMMY_TILE in copy.tiles:
            copy.remove(DUMMY_TILE)

        if copy.size() > 14:
            print(copy.size())
            copy.print()
            print(self.size())
            # self.print()
            raise ValueError(f"Invalid number of tiles: {copy.size()}")

        copy.sort()
        counts = copy.tile_counts()

        pairs = 0
        for c in counts.values():
            if c == 2:
                pairs += 1
        if pairs == 7:
            return True

        def bt(counts, got_pair):
            # print(counts, got_pair)
            total = sum(counts.values())
            # print(total)
            if total == 0:
                return got_pair

            for t in counts.keys():
                if counts[t] >= 3:
                    counts[t] -= 3
                    if bt(counts, got_pair):
                        return True
                    counts[t] += 3

                if counts[t] == 2 and not got_pair:
                    counts[t] -= 2
                    if bt(counts, True):
                        return True
                    counts[t] += 2

                if counts[t] > 0:
                    t2 = t[:-1] + str(int(t[-1]) + 1)
                    t3 = t[:-1] + str(int(t[-1]) + 2)
                    if t2 in counts.keys() and t3 in counts.keys():
                        if counts[t2] >= 1 and counts[t3] >= 1:
                            counts[t] -= 1
                            counts[t2] -= 1
                            counts[t3] -= 1
                            if bt(counts, got_pair):
                                return True
                            counts[t] += 1
                            counts[t2] += 1
                            counts[t3] += 1
            return False

        return bt(counts, False)
    
    def hand_score(self):
        # check suit count
        if len(self.get_tiles_by_suit().keys()) > 2:
            return 0

        counts = self.tile_counts()
        triples = len([
            Tile(tile_str[:-1], tile_str[-1])
            for tile_str in counts.keys()
            if counts[tile_str] >= 3
        ])

        pairs = len([
            Tile(tile_str[:-1], tile_str[-1])
            for tile_str in counts.keys()
            if counts[tile_str] == 2 or counts[tile_str] == 4
        ])

        self.sort()
        seq = 0
        for tile in self.tiles:
            second = Tile(tile.suit_type, str(int(tile.value) + 1))
            third = Tile(tile.suit_type, str(int(tile.value) + 2))
            if (
                self.contains(tile)
                and self.contains(second)
                and self.contains(third)
            ):
                seq += 1
        
        # 10 is arbitrary
        score = (pairs + triples + seq) / 20

        if score > 1:
            raise ValueError("Invalid score:", score)

        return score
