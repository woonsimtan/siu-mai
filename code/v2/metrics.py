import pandas as pd
import numpy as np
import os
from v2.base_game import main as base_game
import math
from datetime import datetime
import itertools
import argparse
import traceback
import time


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
        "-sim",
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

    # wait for other tests to be set up and switch branches before running
    # time.sleep(300)

    startTime = datetime.now()

    # open files

    args = parse_arguments()
    csv_filepath = f"{os.getcwd()}/v2/data/game_history_{args.agents.replace(',', '')}_{args.sim}.csv"

    if os.path.exists(csv_filepath):
        game_hist = pd.read_csv(csv_filepath)
    else:
        game_hist = pd.DataFrame(
            columns=[
                "game",
                "player0_type",
                "player1_type",
                "player2_type",
                "player3_type",
                "player0_score",
                "player1_score",
                "player2_score",
                "player3_score",
            ]
        )
    n = args.n
    save = args.save == "y"
    player_types = generate_player_combinations(args.agents)

    k = len(game_hist)
    failed_games = 0

    for p in player_types:
        for i in range(n):
            print(f"Game {i + player_types.index(p) * n} played: {p}")
            try:
                player_scores = base_game(p, args.sim, True)
                game_n = len(game_hist)
                game_hist.loc[game_n] = [game_n] + p + player_scores

                if save:
                    # save data to files
                    game_hist.to_csv(csv_filepath, index=False)
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

    # for agent in POSSIBLE_AGENTS.values():
    #     if wins[agent][1] != 0:
    #         print(
    #             f"{agent} win rate: {round(wins[agent][0]/wins[agent][1] * 100, 2)}% ({wins[agent][0]} of {wins[agent][1]} games played)"
    #         )

    for agent in POSSIBLE_AGENTS.values():
        if scores[agent][1] != 0:
            print(
                f"{agent} average score: {round(scores[agent][0]/scores[agent][1], 2)}"
            )


if __name__ == "__main__":
    main()
