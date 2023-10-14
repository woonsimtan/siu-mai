# imports
import random

# fixed values
suit_values = {
    "Numbers": ["1", "2", "3", "4", "5", "6", "7", "8", "9"],
    "Circles": ["1", "2", "3", "4", "5", "6", "7", "8", "9"],
    "Bamboo": ["1", "2", "3", "4", "5", "6", "7", "8", "9"],
    "Wind": ["E", "S", "W", "N"],
    "Dragon": ["B", "Z", "F"],
}

flowers = {
    "A": ["1", "2", "3", "4"],
    "B": ["1", "2", "3", "4"],
}


# Tile class definition
class Tile:
    def __init__(self, suit_type, value):
        self.suit_type = suit_type
        self.value = value

    def __eq__(self, other):
        return (self.suit_type == other.suit_type) and (self.value == other.value)


# ignored flowers for now
def create_tiles():
    all_tiles = []
    # for every suit
    for key in suit_values.keys():
        # for every value
        for value in suit_values[key]:
            # create 4 tiles
            for i in range(4):
                all_tiles.append(Tile(key, value))

    # add flowers
    # # for key in flowers.keys():
    # #     for value in flowers[key]:
    # #         all_tiles.append(Tile(key, value))

    # shuffle tiles
    random.shuffle(all_tiles)
    # return list of tiles
    return all_tiles


def print_tiles(tile_list):
    to_print = []
    # sort tiles
    tile_list = sort_tile_list(tile_list)
    # print tiles
    for tile in tile_list:
        to_print.append(tile.suit_type + tile.value)
    print(to_print)


def sort_tile_list(tile_list):
    return sorted(tile_list, key=lambda x: (x.suit_type, x.value), reverse=False)


def tile_lists_equal(tiles1, tiles2):
    tiles1 = sort_tile_list(tiles1)
    tiles2 = sort_tile_list(tiles2)
    return tiles1 == tiles2


class Player:
    def __init__(self, position, hidden_tiles, displayed_tiles):
        self.position = position
        self.hidden_tiles = hidden_tiles
        self.displayed_tiles = displayed_tiles
        # self.ignored_tiles = ignored_tiles

    def print_player_tiles(self):
        print("These are your hidden tiles:")
        print_tiles(self.hidden_tiles)
        print("These are your displayed tiles:")
        print_tiles(self.displayed_tiles)

    def discard(self):
        if self.position == 0:
            print("Please select tile to discard:")
            done = False
            while not done:
                suit = input("Enter suit (Bamboo, Circles, Numbers, Dragon or Wind):")
                value = input("Enter value:")
                tile_to_discard = Tile(suit, value)
                if tile_to_discard in self.hidden_tiles:
                    self.hidden_tiles.remove(tile_to_discard)
                    done = True
        else:
            tile_to_discard = self.hidden_tiles[
                random.randint(0, len(self.hidden_tiles) - 1)
            ]
            self.hidden_tiles.remove(tile_to_discard)
        return tile_to_discard

    def chi(self, tile):
        done = False
        while not done:
            suit = tile.suit_type
            tile1_value = input("enter tile 1 value: ")
            tile2_value = input("enter tile 2 value: ")
            if (
                Tile(suit, tile1_value) in self.hidden_tiles
                and Tile(suit, tile2_value) in self.hidden_tiles
            ):
                # TODO: insert check that is a valid sequence
                self.hidden_tiles.remove(Tile(suit, tile1_value))
                self.hidden_tiles.remove(Tile(suit, tile2_value))
                self.displayed_tiles += sort_tile_list(
                    [tile, Tile(suit, tile1_value), Tile(suit, tile2_value)]
                )
                done = True
            else:
                print("Invalid chi")
        self.print_player_tiles()

    def peng(self, tile):
        for i in range(2):
            self.hidden_tiles.remove(tile)
        self.displayed_tiles += [tile, tile, tile]
        self.print_player_tiles()

    # ignore gong for now
    # # def gong(self, tile):
    # #     for i in range(3):
    # #         self.hidden_tiles.remove(tile)
    # #     self.displayed_tiles.append([tile, tile, tile, tile])

    def win(self, new_tile):
        # win by any 4 sets of 3 and a pair
        # know displayed tiles are already sets of 3
        # so only need to check hidden tiles

        tile_list = sort_tile_list(self.hidden_tiles.copy() + [new_tile])
        tile_set = []
        for tile in tile_list:
            if tile not in tile_set:
                tile_set.append(tile)

        possible_pairs = []
        for tile in tile_set:
            if tile_list.count(tile) >= 2:
                possible_pairs.append(tile)

        for pair in possible_pairs:
            test_list = tile_list.copy()
            test_list.remove(pair)
            test_list.remove(pair)
            # remaining is either part of sequence or part of triplet
            while len(test_list) > 0:
                tile = test_list[0]
                if test_list.count(tile) < 3 and (
                    tile.suit_type in ["Numbers", "Bamboo", "Circles"]
                ):
                    tile2 = Tile(tile.suit_type, str(int(tile.value) + 1))
                    tile3 = Tile(tile.suit_type, str(int(tile.value) + 2))
                    if tile2 in test_list and tile3 in test_list:
                        test_list.remove(tile)
                        test_list.remove(tile2)
                        test_list.remove(tile3)
                    else:
                        break
                elif test_list.count(tile) < 3:
                    break
                else:  # because sorted so if appears more than twice has to be part of triplet?
                    test_list.remove(tile)
                    test_list.remove(tile)
                    test_list.remove(tile)
            if len(test_list) == 0:  # if while loop terminated naturally then valid win
                return True

        return False


def game_setup(all_tiles):
    # distribute tiles
    players = []
    player_tiles = [[], [], [], []]
    for i in range(3):
        for j in range(4):
            for k in range(4):
                player_tiles[j].append(all_tiles[j * 4 + k])
        all_tiles = all_tiles[16:]
    for i in range(4):
        player_tiles[i].append(all_tiles[i])
    all_tiles = all_tiles[4:]
    # set up players
    for i in range(4):
        tiles = player_tiles[i]
        sort_tile_list(tiles)
        players.append(Player(i, tiles, []))
    return players, all_tiles


def pickup_tile(all_tiles):
    return all_tiles.pop(0)


def check_for_win(players, discarded_tile):
    if discarded_tile != discarded_tile:
        return False
    for player in players:
        if player.win(discarded_tile):
            print("Player " + str(players.index(player)) + " has won!")
            #
            player.hidden_tiles.append(discarded_tile)
            player.print_player_tiles()
            #
            return True
        else:
            pass
    return False


def check_for_chi(player_tiles, discarded_tile):
    if discarded_tile != discarded_tile:
        return False
    if discarded_tile.suit_type != "Wind" and discarded_tile.suit_type != "Dragon":
        wanted_tiles = []
        for i in range(5):
            wanted_tiles.append(
                Tile(discarded_tile.suit_type, str(int(discarded_tile.value) - 2 + i))
            )
        wanted_tiles = sort_tile_list(wanted_tiles)
        new_tile_set = player_tiles.copy()
        new_tile_set.append(discarded_tile)
        for i in range(3):
            if (
                (wanted_tiles[i] in new_tile_set)
                and (wanted_tiles[i + 1] in new_tile_set)
                and (wanted_tiles[i + 2] in new_tile_set)
            ):
                return True
    return False


def check_for_peng(players, discarded_tile):
    if discarded_tile != discarded_tile:
        return False, float("NaN")
    for player in players:
        if player.hidden_tiles.count(discarded_tile) >= 2:
            # print("Player " + str(players.index(player)) + " PENG")
            return True, players.index(player)
    return False, float("NaN")


# have ignored gong to begin with
# # def check_for_gong(discarded_tile):
# #     return False






def main():
    # gameplay for single round

    # set initial values
    round = 0
    prevailing = "E"
    player_number = 0  # change this to player who's position is east
    all_tiles = create_tiles()
    players, all_tiles = game_setup(all_tiles)
    discarded_tiles = []
    last_discarded = float("NaN")
    try:
        while not check_for_win(players, last_discarded) and len(all_tiles) > 0:

            peng, new_player_number = check_for_peng(players, last_discarded)
            if peng:
                if new_player_number == 0:
                    players[new_player_number].print_player_tiles()
                    print(
                        "You can peng. Would you like to peng? (Enter 1 if yes, 0 if no): "
                    )
                    yes = int(input())
                else:  # assume bot will always choose to peng
                    # yes = random.randint(0, 1)
                    yes = 1
                peng = peng and (yes == 1)
                if peng:
                    player_number = new_player_number

            chi = check_for_chi(players[player_number].hidden_tiles, last_discarded)
            if chi:
                if player_number == 0:
                    players[player_number].print_player_tiles()
                    print(
                        "You can chi. Would you like to chi? (Enter 1 if yes, 0 if no): "
                    )
                    yes = int(input())
                else:  # bot will always choose not to chi because not coded which sequence it will take the tile for
                    # yes = random.randint(0, 1)
                    yes = 0
                chi = chi and (yes == 1)

            if peng:
                players[player_number].peng(last_discarded)
                last_discarded = players[player_number].discard()

            if not peng and chi:
                players[player_number].chi(last_discarded)
                last_discarded = players[player_number].discard()

            if not peng and not chi:
                if last_discarded == last_discarded:
                    discarded_tiles.append(last_discarded)
                print("Player" + str(player_number))
                new_tile = pickup_tile(all_tiles)
                print("You picked up:")
                print_tiles([new_tile])
                if players[player_number].win(new_tile):
                    break

                players[player_number].hidden_tiles.append(new_tile)
                players[player_number].print_player_tiles()
                last_discarded = players[player_number].discard()
            player_number = (player_number + 1) % 4

            print("--------")
            print("This tile has been discarded:")
            print_tiles([last_discarded])
            print("These are all the previously discarded tiles:")
            print_tiles(discarded_tiles)
            print("--------")

        if len(all_tiles) == 0:
            print("Nobody won")

    except Exception as e:
        print(e)