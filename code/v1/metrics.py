import pandas as pd
import os
from v1.base_game import main as base_game
import math

wins = {}
PLAYER_MAPPING = {0: "player0", 1: "player1", 2: "player2", 3: "player3"}


def add_to_wins(row):
    for p in PLAYER_MAPPING.values():
        wins[row[p]][1] += 1

    if not math.isnan(row["winning_player"]):
        winner = row[PLAYER_MAPPING[int(row["winning_player"])]]
        wins[winner][0] += 1


def win_rate(data, agent_types):
    for agent in agent_types:
        wins[agent] = [0, 0]  # games won, games played

    data.apply(lambda x: add_to_wins(x), axis=1)


def main():
    # open files
    game_hist = pd.read_csv(os.getcwd() + "\\" + "v1\game_history.csv")

    # set number of games to run
    n = 100
    player_types = ["RANDOM", "RANDOM", "RANDOM", "RANDOM"]

    for i in range(n):
        winning_player = base_game(player_types)
        game_n = len(game_hist)
        game_hist.loc[game_n] = [game_n, winning_player] + player_types

    # save data to files
    game_hist.to_csv(os.getcwd() + "\\" + "v1\game_history.csv", index=False)

    # summarize data
    possible_agents = ["RANDOM"]
    win_rate(game_hist, possible_agents)

    for agent in possible_agents:
        if wins[agent][1] != 0:
            print(
                f"{agent} win rate: {round(wins[agent][0]/wins[agent][1] * 100)}% ({wins[agent][0]} of {wins[agent][1]} games played)"
            )
