# V1 Design

This document contains the low-level design of the code files in the `V1` folder.

## Game Set-up

### tiles.py

The `Tile` class is created to represent a single mahjong tile. It has the following properties:

- `suit_type` = string
- `value` = numeric value represented as a string

The following functions are defined for a `Tile`:

- `__eq__` - two tiles are equal if they have the same suit and same value
- `__lt__` - A is less than B if A has a smaller suit or a smaller value
- `to_string` returns a string representation of the tile
- `print` outputs the tile in terminal.
- `copy` returns a new identical Tile

An extra `DUMMY_TILE` has been defined for use as a placeholder. Checks have been implemented to remove them from a player's hand when identified.

The `TileList` class is created to represent a list of mahjong tiles. It has the following properties:

- `tiles` = list of `Tile` objects

Note: Supposed to be initialised as empty if tiles is not specified but had issues so should be initialised as `TileList([])` if necessary.

The following functions are defined for a `TileList`

- `__eq__` returns if the provided lists are the same.
- `sort` sorts tiles by suit type and value, does not return anything.
- `print_form` returns a list of strings, representing sorted tiles in a list.
- `print` outputs the list in terminal.
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

### game_state.py

Defines a `GameState` for the purpose of gameplay and MCTS.

The following properties are defined:

- `deck`
- `players`
- `discarded_tiles`
- `last_discarded`
- `current_player_number`

The following functions are defined:

- `print` outputs in the terminal all the tiles each player has in their hand, along with the current player number and the last discarded tile.
- `any_peng` checks if any players can peng.
- `any_wins` checks if any players can win on the discarded tile.
- `game_result` returns a value depending on the maximising player and the game state corresponding to a win, tie or loss.
- `ended` returns if the deck has been emptied or if a player has won.
- `get_legal_actions` returns the list of actions that a player can choose to carry out.
- `get_next_action` ???
- `initialise_mcts_state` returns a game state proposed by the MCTS agent based on the information it currently has available.
- `get_tiles_hidden_from_player` returns a list of

### base_game.py

The following functions are defined to setup and run the game:

- `create_tiles` creates all tiles required and shuffles them.
- `distribute_tiles` takes out 13 tiles for each player.
- `any_peng` checks for a possible peng by any player.
- `any_wins` checks for a possible win by any player.
- `setup_players` puts each player into the list, creating an agent for each specified type.
- `main` runs gameplay.

## Agents (players.py)

Player has been implemented as an abstract class with the following properties defined:

- `possible_discards`
- `displayed_tiles`

The following functions have also been defined for them:

- `pickup` adds a new tile to possible discards.
- `all_tiles` returns all tiles that the agent holds.
- `check_for_win` checks for a win using all the tiles that the agent holds.
- `check_for_peng` checks if the agent can choose to carry out PENG given a tile.
- `choose_peng` returns a boolean for whether the agent should PENG.
- `peng` shifts the tiles for the move into the list of displayed tiles and removes them from possible discards.
- `discard` selects a tile to discard.
- `get_hidden_tiles` returns tiles that the agent has that are hidden from other players.
- `total_tile_count` returns total number of tiles the agent holds.
- `is_mcts` returns if the agent is a MCTS agent.

### RandomAgent

The RandomAgent extends the Player class without any changes.

- It will PENG when possible.
- It will randomly select a discard tile from all of the possible discards in its hand.

### SemiRandomAgent

The SemiRandomAgent extends the Player class with some changes. The logic that the semi-random agent follows is as below:

- Tiles will be grouped into sets of three where possible (three of a kind or a sequence of the same suit).
- A pair will be retained at first opportunity.
- Tiles which are in a group or in a pair are locked in the players hand and will not be discarded.
- The discarded tile will be randomly selected amongst the remaining tiles in the player's hand.

**TODO:** assert if the agent is discarding a random tile from an expected hand.

The following extra properties are defined for the agent:

- `pair` = TileList containing a pair of identical tiles.
- `locked_tiles` = TileList containing tiles that will not be discarded.

The following functions are defined for the agent:

- `all_tiles` returns a complete TileList of all the tiles the agent holds.
- `get_hidden_tiles` returns all of the tiles hidden from other players.
- `pickup` adds a tile to the player's hand and checks for tiles to lock.
- `lock_three_of_a_kind` checks for 3 of the same tiles within the agent's hand, takes them out of the possible discard pile and locks them.
- `lock_three_consecutive` checks for 3 consecutive tiles from the same suit within the agent's hand, takes them out of the possible discard pile and locks them.
- `lock_triples` locks both three of a kind and consecutive tiles.
- `lock_pair` checks for pairs in the players hand, selecting a random pair if there are multiple, and locks those.

### MCTSAgent

The MCTSAgent extends the player class with some changes. It utilises Monte Carlo Tree Search as implemented in `mcts.py`.

The following extra properties are defined for the agent:

- `player_number`

The following functions are defined for the agent:

- `discard` creates a MonteCarloTreeSearch node and searches for the best action, returning the tile chosen for discard.
- `is_mcts` returns True

**TODO:** implement function for deciding if the agent should PENG.

## MCTS set-up

This utilises skeleton code taken from [an MCTS tutorial](https://github.com/ai-boson/mcts).
