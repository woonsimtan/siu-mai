# V1 Design

This document contains the low-level design of the code files in the `V1` folder.

## tiles.py

The `Tile` class is created to represent a single mahjong tile. It has the following properties:

- `suit_type` = string
- `value` = numeric value represented as a string

The following functions are defined for a `Tile`:

- `__eq__` - two tiles are equal if they have the same suit and same value
- `__lt__` - A is less than B if A has a smaller suit or a smaller value
- `to_string` - returns a string representation of the tile

An extra `DUMMY_TILE` has been defined for use in initialising the game.

The `TileList` class is created to represent a list of mahjong tiles. It has the following properties:

- `tiles` = list of `Tile` objects, initialised to be empty unless specified.

The following functions are defined for a `TileList` -`sort` sorts tiles by suit type and value, does not return anything.

- `print_form` returns a list of strings, representing sorted tiles in a list.
- `add` adds a single tile into the list.
- `add_tiles` adds a given `TileList` into the list.
- `shuffle` mixes up the order of tiles randomly.
- `remove` tries to remove a single tile from the list, raising a `ValueError` if the tile to be removed is not found in the list.
- `remove_tiles` removes a given `TileList` from the list.
- `size` returns the number of tiles in the list.
- `unique_tiles` returns a `TileList` of the unique tiles contained in the list.
- `tile_counts` returns a dictionary of the counts of each individual tile mapped to the string representation of the tile.
- `remove_random_tile` removes a random tile from the list.
- `contains` takes a tile and returns if the tile is in the list.
- `check_for_peng` checks if there are already 2 of the given tiles in the list, thus returning if peng is a possible move.
- `count` takes a list and returns the number of occurences of the tile in the list.
- `copy` returns a new `TileList` with the same set of tiles
- `check_for_win` takes a tile and examines if the list is a winning hand with the addition of this new tile.

## base_game.py

## random_agent.py
