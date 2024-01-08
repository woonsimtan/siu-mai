# Code

This document covers high level design of the code files in this repository.

## High-level structure

- `poetry` files to manage package dependencies.
- `v1` folder contains code for the first iteration of the base game, along with a random agent.
- `v2` and `v3` folders will be created later on in the project (poetry file will need to be updated with these folder nams for developement).
- `tests` contains unit tests for all code files.

## Version 1

- `base_game.py` contains main logic for the game to function.
- `tiles.py` contains objects created for the base game to function.
- `random_agent` contains a completely random agent along with a semi-random agent, both of which randomly select tiles from a set of possible discards.
- `mcts_node.py` contains logic for the MCTS agent to follow.
- `mcts_agent.py` contains functions implemented for an agent using logic for MCTS to play the game.
- `metrics.py` runs the base game for a determined number of times and saves game history to a csv file.
