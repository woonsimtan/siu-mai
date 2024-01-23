# CS344 Siu-MAI: The Sichuan Mahjong AI

3rd Year Discrete Mathematics Project by Leia Tan

## Description

The objective of this project is to develop an agent to play Mahjong using Monte Carlo Tree Search. This is done with 3 iterations of the rules, increasing in difficulty. The [rules](http://www.mahjong-mil.org/pdf/Brief_Introduction_to_Bloody_Mahjong.pdf) followed are provided by the Mahjong International League with the following adaptations for each iteration:

1. Ignore all scoring and a single round of the game will end when a single player has won. The agent's goal is to end the game with a winning hand.
2. Implement win scoring. The agent will be trying to maximise its win.
3. Allow other players to keep playing after someone wins. The game will end when three players have won or when the wall is exhausted. Wall exhaustion scoring will also be implemented. Similarly to the second iteration, the agent will aim to maximise its win.

## Run the code

### Initialising the base game with 4 random agents

- `cd code`
- `poetry install`
- `poetry run base_game`

### Initialising the game for each combination of agents

- `poetry run metrics -n <number-of-games> -save <y/n>`

### Testing a single game

- Update the list of agent types in base_game.py
- `poetry run review`

### Testing during development

- `poetry run coverage run -m pytest; poetry run coverage report -m`

## Notes

**BUG:** MCTS agent mostly discarding the tile it just picked up. Perhaps should do tree search built on semi random agent?

**BUG:** MCTS fails sometimes - search hits a point where not terminal node but has no children

### Runtimes

4 MCTS Agents in a single game

- 10 simulations -> 39s
- 100 simulations -> 6 mins
- 1000 simulations -> 1h
- 10k simulations -> ~10h

Requires 25mins to run all combinations of agents, with some games failing and 10 simulations.
