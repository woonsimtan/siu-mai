import pandas as pd
import numpy as np
import os
from v1.base_game import main as base_game
import math
from datetime import datetime
import itertools
import argparse

wins = {}
PLAYER_MAPPING = {0: "player0", 1: "player1", 2: "player2", 3: "player3"}
POSSIBLE_AGENTS = ["RANDOM", "MCTS", "SEMIRANDOM"]


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

    # for p in PLAYER_MAPPING.values():
    #     wins[row[p]][1] += 1

    # winner
    if not math.isnan(row["winning_player"]):
        winner = int(row["winning_player"])
        for agent, chosen_player in chosen.items():
            if chosen_player == winner:
                wins[agent][0] += 1

        # winner = row[PLAYER_MAPPING[int(row["winning_player"])]]
        # i
        # wins[winner][0] += 1


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
        "-save",
        help="If data should be saved to csv (y/n)",
        type=str,
        required=False,
        default="y",
    )
    return parser.parse_args()


def main():
    startTime = datetime.now()

    # open files
    game_hist = pd.read_csv(os.getcwd() + "\\" + "v1\game_history.csv")
    args = parse_arguments()

    n = args.n
    player_types = generate_player_combinations()

    k = len(game_hist)
    failed_games = 0

    for p in player_types:
        for i in range(n):
            print(f"Game {i + player_types.index(p) * n} played")
            try:
                winning_player = base_game(p)
                game_n = len(game_hist)
                game_hist.loc[game_n] = [game_n, winning_player] + p

                if args.save == "y":
                    # save data to files
                    game_hist.to_csv(
                        os.getcwd() + "\\" + "v1\game_history.csv", index=False
                    )
            except Exception as e:
                print(e)
                failed_games += 1
                continue

    print("")
    print(f"{len(player_types) * n} games were run in {datetime.now() - startTime}.")
    print(f"{failed_games} failed to fully run.")

    # summarize data

    x = k - failed_games
    game_hist = game_hist[x:]

    win_rate(game_hist)

    for agent in POSSIBLE_AGENTS:
        if wins[agent][1] != 0:
            print(
                f"{agent} win rate: {round(wins[agent][0]/wins[agent][1] * 100, 2)}% ({wins[agent][0]} of {wins[agent][1]} games played)"
            )
