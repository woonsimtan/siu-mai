# CS344 Siu-MAI: The Sichuan Mahjong AI

3rd Year Discrete Mathematics Project by Leia Tan

## Description

The objective of this project is to develop an agent to play Mahjong using Monte Carlo Tree Search. This is done with 3 iterations of the rules, increasing in difficulty. The [rules](http://www.mahjong-mil.org/pdf/Brief_Introduction_to_Bloody_Mahjong.pdf) followed are provided by the Mahjong International League with the following adaptations for each iteration:

1. Ignore all scoring and a single round of the game will end when a single player has won. The agent's goal is to end the game with a winning hand.
2. Implement win scoring. The agent will be trying to maximise its win.
3. Allow other players to keep playing after someone wins. The game will end when three players have won or when the wall is exhausted. Wall exhaustion scoring will also be implemented. Similarly to the second iteration, the agent will aim to maximise its win.

## Run the code on DCS Machines

- `python3 code/v1/metrics.py -n <number-of-games> -save <y/n> -csv <filename> -completed <number-of-completed-games-required-for-mcts>`

### Batch compute on DCS

- `sbatch dcs.sbatch` to send a job
- `sacct --format JobId,State,MaxRSS,Elapsed,CPUTime,Start,End,Reason` to see submitted jobs
- `seff <job-id>` to see details of individual job
- `scancel <job-id>` to kill the job

## Run the code on own laptop

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

**BUG (14.02.2024 update: to be reviewed again if this still happens):** MCTS agent mostly discarding the tile it just picked up.
Win rate generally is very low (~6%?) so it means many of the options have the same weights. Explains the bad performance of the agent. Might make sense to pick from a narrowed down list of possible discards so more simulations are run on "better" discards? Still need to understand though if there is something that means the tile that just got picked up is more likely to be picked.

**BUG (14.02.2024):** Sometimes after PENG players end up with 16 tiles - adding tiles to the wrong player but why?

**FIXED - BUG (14.02.2024):** Bug where tiles of unwanted suit is still showing in the player's hand. Not sure why this is happening. Previously thought this was because the unwanted suit was changing when mcts was initiated. Possibly this wasn't completely fixed? But could also be due to another reason? The games run without issues when it's only rule-based agents so the issue must lie in some part of the mcts implementation.

- Agent is back to playing fixed number of simulations instead of number of games that have a winner.

### Runtimes

4 MCTS Agents in a single game

- 10 simulations -> 39s
- 100 simulations -> 6 mins
- 1000 simulations -> 1h
- 10k simulations -> ~10h

Requires 25mins to run all combinations of agents, with some games failing and 10 simulations.
