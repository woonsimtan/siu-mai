import pandas as pd
import os

def wipe_data():
    for file in os.listdir(f"{os.getcwd()}/code/v2/data/"):
        game_hist = pd.read_csv(f"{os.getcwd()}/code/v2/data/{file}")
        game_hist["winning_score"] = 0
        game_hist = game_hist.head(0)
        game_hist.to_csv(
            os.getcwd() + "/" + f"code/v2/data/{file}", index=False
        )