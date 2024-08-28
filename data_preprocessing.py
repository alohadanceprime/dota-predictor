import pandas as pd
import glob
import os
import requests


def load_matches_from_folder(folder_path: str) -> pd.DataFrame:
    """
    Loads csvs from folder and merges to one dataframe

    """
    return pd.concat(
        (pd.read_csv(file) for file in glob.glob(os.path.join(folder_path, '*.csv'))),
        ignore_index=True)


def get_heroes():
    """
    Returns heroes decode dict
    Needs ethernet connection for connect to opendota API

    """
    url = "https://api.opendota.com/api/heroes"
    response = requests.get(url)
    if response.status_code == 200:
        heroes = response.json()
        hero_dict = {hero['id']: hero['localized_name'] for hero in heroes}
        return hero_dict
    else:
        raise Exception("Unavailable opendota API")


def to_new_rank_tier_system(ex_rank: int) -> int:
    return (ex_rank // 10 - 1) * 5 + ex_rank % 10


heroes_dict = get_heroes()

print("Enter path to csvs folder")
path = input()
df = load_matches_from_folder(path)
df.drop(["ID", "duration", "num_rank_tier"], axis=1, inplace=True)
df = df[(df["lobby_type"] == 7) & (df['game_mode'] == 22)]
df.drop(["lobby_type", "game_mode"], axis=1, inplace=True)
df["avg_rank_tier"] = df["avg_rank_tier"].apply(to_new_rank_tier_system)
df.to_csv("data.csv", index=False)
