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

Note: `check_for_win` could do with additional testing.

## base_game.py

TODO: add functionality to save game data

The following functions are defined to setup and run the game:

- `create_tiles` creates all tiles required and shuffles them.
- `distribute_tiles` takes out 13 tiles for each player.
- `any_peng` checks for a possible peng by any player.
- `any_wins` checks for a possible win by any player.
- `setup_players` puts each player into the list, creating an agent for each specified type.
- `main` runs gameplay.

## random_agent.py

The logic that the agent follows is as below:

- Tiles will be grouped into sets of three where possible (three of a kind or a sequence of the same suit).
- A pair will be retained at first opportunity.
- Tiles which are in a group or in a pair are locked in the players hand and will not be discarded.
- The discarded tile will be randomly selected amongst the remaining tiles in the player's hand.

Note: the agent is not discarding from a random tile from an expected hand - this could be a point of failure in implementation, but it is not blocking and the agent can still win.

The following properties are defined for the agent:

- `pair` = TileList containing a pair of identical tiles.
- `locked_tiles` = TileList containing tiles that will not be discarded.
- `possible_discards` = TileList from which the agent selects a tile to randomly discard
- `displayed_tiles` = Results of peng moves during the game.

The following functions are defined for the agent:

- `all_tiles` returns a complete TileList of all the tiles the agent holds.
- `total_tile_count` returns count of all tiles held.
- `play_a_turn` checks for a possible win based on the picked up tile, and returns a dummy tile if so, otherwise checks for triples and pairs to lock, and randomly selects a discard tile.
- `discard` removes a randomly selected tile and returns it.
- `lock_three_of_a_kind` checks for 3 of the same tiles within the agent's hand, takes them out of the possible discard pile and locks them.
- `lock_three_of_a_kind` checks for 3 consecutive tiles from the same suit within the agent's hand, takes them out of the possible discard pile and locks them.
- `lock_triples` locks both three of a kind and consecutive tiles.
- `lock_pair` checks for pairs in the players hand, selecting a random pair if there are multiple, and locks those.
- `check_for_win` checks for a winning hand with all of the agent's tiles.
- `check_for_peng` checks if the agent can peng based on their hand.
- `peng` shifts tiles into display, and discards a tile.

## mcts_node.py and mcts_agent.py

should have a node for peng/no peng and selecting discard tile
