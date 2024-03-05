import pandas as pd
import numpy as np
import os
from v3.base_game import main as base_game
from datetime import datetime
import itertools
import argparse
import traceback


scores = {}
PLAYER_MAPPING = {0: "player0", 1: "player1", 2: "player2", 3: "player3"}
POSSIBLE_AGENTS = {"m": "MCTS", "s": "SEMIRANDOM", "r": "RANDOM", "h": "HANDSCORE"}


def add_to_wins(row):
    # select random player for each agent type
    players = {}
    for p in POSSIBLE_AGENTS.values():
        players[p] = []

    for i in range(4):
        players[row[f"{PLAYER_MAPPING[i]}_type"]].append(i)

    chosen = {}
    for key, value in players.items():
        if len(value) != 0:
            chosen[key] = players[key][np.random.randint(len(players[key]))]

    # number of games played
    for p in chosen.keys():
        scores[p][1] += 1

    # add score for selected player
    for agent, chosen_player in chosen.items():
        scores[agent][0] += row[f"player{chosen_player}_score"]


def win_rate(data):
    for agent in POSSIBLE_AGENTS.values():
        scores[agent] = [0, 0]  # games won, games played

    data.apply(lambda x: add_to_wins(x), axis=1)


def generate_player_combinations(agent_input):
    if agent_input == "all":
        combs = list(
            itertools.combinations_with_replacement(list(POSSIBLE_AGENTS.values()), 4)
        )
        list_ver = [list(comb) for comb in combs]
        return list_ver
    else:
        # process input string
        return [[POSSIBLE_AGENTS[i] for i in agent_input.split(",")]]


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-n",
        help="Number of games to run for each combination of agents",
        type=int,
        required=False,
        default=0,
    )
    parser.add_argument(
        "-completed",
        help="Number of simulations the MCTS agent is supposed to run",
        type=int,
        required=False,
        default=10,
    )
    parser.add_argument(
        "-save",
        help="If data should be saved to csv (y/n)",
        type=str,
        required=False,
        default="n",
    )
    parser.add_argument(
        "-csv",
        help="name of the csv file that game data should be saved to",
        type=str,
        required=False,
        default="game_history",
    )
    parser.add_argument(
        "-agents",
        help="combination of agents to play",
        type=str,
        required=False,
        default="all",
    )
    return parser.parse_args()


def main():

    startTime = datetime.now()

    # open files

    args = parse_arguments()
    game_hist = pd.read_csv(f"{os.getcwd()}/v3/data/{args.csv}.csv")

    n = args.n
    save = args.save == "y"
    player_types = generate_player_combinations(args.agents)

    k = len(game_hist)
    failed_games = 0

    for p in player_types:
        for i in range(n):
            print(f"Game {i + player_types.index(p) * n} played: {p}")
            try:
                game_output = base_game(p, args.completed, True)
                game_n = len(game_hist)
                game_hist.loc[game_n] = [game_n] + p + game_output

                if save:
                    # save data to files
                    game_hist.to_csv(
                        os.getcwd() + "/" + f"v3/data/{args.csv}.csv", index=False
                    )
            except Exception as e:
                print(e)
                print(p)
                traceback.print_exc()
                failed_games += 1
                continue

    print("")
    print(f"{len(player_types) * n} games were run in {datetime.now() - startTime}.")
    print(f"{failed_games} failed to fully run.")

    # summarize data

    # only show output of newly played games
    if n != 0:
        x = k - failed_games
        game_hist = game_hist[x:]

    win_rate(game_hist)

    for agent in POSSIBLE_AGENTS.values():
        if scores[agent][1] != 0:
            print(
                f"{agent} average score: {round(scores[agent][0]/scores[agent][1], 2)}"
            )


if __name__ == "__main__":
    main()
