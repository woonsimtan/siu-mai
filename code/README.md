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
- `random_agent` contains an agent to play the base game and discards random tiles on each turn.
