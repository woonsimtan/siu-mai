import pandas as pd
import os

def wipe_data():
    for file in os.listdir(f"{os.getcwd()}/code/v3/data/"):
        # game_hist = pd.read_csv(f"{os.getcwd()}/code/v3/data/{file}")
        game_hist = pd.read_csv(f"{os.getcwd()}/code/v3/game_history.csv")
        game_hist = game_hist.head(0)
        game_hist.to_csv(
            os.getcwd() + "/" + f"code/v3/data/{file}", index=False
        )

wipe_data()