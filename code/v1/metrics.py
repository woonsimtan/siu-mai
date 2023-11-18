import pandas as pd
import numpy as np
import os
from v1.base_game import main as base_game
import math

wins = {}
PLAYER_MAPPING = {0: "player0", 1: "player1", 2: "player2", 3: "player3"}
possible_agents = ["RANDOM", "MCTS"]


def add_to_wins(row):
    # select random player for each agent type
    players = {}
    for p in possible_agents:
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


def win_rate(data, agent_types):
    for agent in agent_types:
        wins[agent] = [0, 0]  # games won, games played

    data.apply(lambda x: add_to_wins(x), axis=1)


def main():
    # open files
    game_hist = pd.read_csv(os.getcwd() + "\\" + "v1\game_history.csv")

    # set number of games to run
    n = 10
    player_types = [
        ["MCTS", "MCTS", "MCTS", "MCTS"],
        ["MCTS", "MCTS", "MCTS", "RANDOM"],
        ["MCTS", "MCTS", "RANDOM", "RANDOM"],
        ["MCTS", "RANDOM", "RANDOM", "RANDOM"],
        ["RANDOM", "RANDOM", "RANDOM", "RANDOM"],
    ]

    for p in player_types:
        for i in range(n):
            print(f"Game {i + player_types.index(p) * n} played")
            try:
                winning_player = base_game(p)
                game_n = len(game_hist)
                game_hist.loc[game_n] = [game_n, winning_player] + p

                # save data to files
                game_hist.to_csv(
                    os.getcwd() + "\\" + "v1\game_history.csv", index=False
                )
            except:
                continue

    # summarize data

    win_rate(game_hist, possible_agents)

    for agent in possible_agents:
        if wins[agent][1] != 0:
            print(
                f"{agent} win rate: {round(wins[agent][0]/wins[agent][1] * 100)}% ({wins[agent][0]} of {wins[agent][1]} games played)"
            )
