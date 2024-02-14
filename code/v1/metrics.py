import pandas as pd
import numpy as np
import os
from v1.base_game import main as base_game
import math
from datetime import datetime
import itertools
import argparse
import traceback


wins = {}
PLAYER_MAPPING = {0: "player0", 1: "player1", 2: "player2", 3: "player3"}
# POSSIBLE_AGENTS = ["RANDOM", "SEMIRANDOM"]  # "MCTS"]
POSSIBLE_AGENTS = ["MCTS"]


def add_to_wins(row):
    # select random player for each agent type
    players = {}
    for p in POSSIBLE_AGENTS:
        players[p] = []

    for i in range(4):
        players[row[PLAYER_MAPPING[i]]].append(i)

    chosen = {}
    for key, value in players.items():
        if len(value) != 0:
            chosen[key] = players[key][np.random.randint(len(players[key]))]

    # games played
    for p in chosen.keys():
        wins[p][1] += 1

    # winner
    if not math.isnan(row["winning_player"]):
        winner = int(row["winning_player"])
        for agent, chosen_player in chosen.items():
            if chosen_player == winner:
                wins[agent][0] += 1


def win_rate(data):
    for agent in POSSIBLE_AGENTS:
        wins[agent] = [0, 0]  # games won, games played

    data.apply(lambda x: add_to_wins(x), axis=1)


def generate_player_combinations():
    combs = list(itertools.combinations_with_replacement(POSSIBLE_AGENTS, 4))
    list_ver = [list(comb) for comb in combs]
    return list_ver


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
        help="Number of completed games the MCTS agent is supposed to run",
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
    return parser.parse_args()


def main():
    startTime = datetime.now()

    # open files

    args = parse_arguments()
    game_hist = pd.read_csv(f"{os.getcwd()}/v1/{args.csv}.csv")

    n = args.n
    save = args.save == "y"
    player_types = generate_player_combinations()

    k = len(game_hist)
    failed_games = 0

    for p in player_types:
        for i in range(n):
            print(f"Game {i + player_types.index(p) * n} played")
            try:
                winning_player = base_game(p, args.completed, True)
                game_n = len(game_hist)
                game_hist.loc[game_n] = [game_n, winning_player] + p

                if save:
                    # save data to files
                    game_hist.to_csv(
                        os.getcwd() + "/" + f"/v1/{args.csv}.csv", index=False
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

    for agent in POSSIBLE_AGENTS:
        if wins[agent][1] != 0:
            print(
                f"{agent} win rate: {round(wins[agent][0]/wins[agent][1] * 100, 2)}% ({wins[agent][0]} of {wins[agent][1]} games played)"
            )


if __name__ == "__main__":
    main()
