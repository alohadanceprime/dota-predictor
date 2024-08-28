import requests
import pandas as pd
import time


def get_recent_public_matches():
    url = "https://api.opendota.com/api/publicMatches"
    response = requests.get(url)
    if response.status_code == 200:
        matches = response.json()
        return matches
    else:
        return None


data = {
    "ID": [],
    'radiant_win': [],
    'duration': [],
    'lobby_type': [],
    'game_mode': [],
    'avg_rank_tier': [],
    'num_rank_tier': [],
    'radiant_teammate_0': [],
    'radiant_teammate_1': [],
    'radiant_teammate_2': [],
    'radiant_teammate_3': [],
    'radiant_teammate_4': [],
    'dire_teammate_0': [],
    'dire_teammate_1': [],
    'dire_teammate_2': [],
    'dire_teammate_3': [],
    'dire_teammate_4': []
}
count = 0
start_time = time.time()
ids = []
total_matches = 0

print("Where to save csvs?")
path = input()

while True:
    recent_matches = get_recent_public_matches()
    if recent_matches:
        for match in recent_matches:
            if match["match_id"] not in ids:
                total_matches += 1
                ids.append(match["match_id"])
                if len(ids) > 100_000:
                    ids.pop(0)
                data["ID"].append(match["match_id"])
                data['radiant_win'].append(match['radiant_win'])
                data['duration'].append(match['duration'])
                data['lobby_type'].append(match['lobby_type'])
                data['game_mode'].append(match['game_mode'])
                data['avg_rank_tier'].append(match['avg_rank_tier'])
                data['num_rank_tier'].append(match['num_rank_tier'])
                for i in range(len(match["radiant_team"])):
                    data[f'radiant_teammate_{i}'].append(match["radiant_team"][i])
                for i in range(len(match["dire_team"])):
                    data[f'dire_teammate_{i}'].append(match["dire_team"][i])
    else:
        print("Cant get data")
        continue
    print(f"Matches collected in pack {len(data["ID"])}; Time elapsed {time.time()-start_time}; Total matches collected {total_matches}")
    if len(data["ID"]) >= 100:
        df = pd.DataFrame(data)
        df.to_csv(path + f"\\matchesdota_matches_pt_{count}.csv", index=False)
        count += 1
        data = {
            "ID": [],
            'radiant_win': [],
            'duration': [],
            'lobby_type': [],
            'game_mode': [],
            'avg_rank_tier': [],
            'num_rank_tier': [],
            'radiant_teammate_0': [],
            'radiant_teammate_1': [],
            'radiant_teammate_2': [],
            'radiant_teammate_3': [],
            'radiant_teammate_4': [],
            'dire_teammate_0': [],
            'dire_teammate_1': [],
            'dire_teammate_2': [],
            'dire_teammate_3': [],
            'dire_teammate_4': []
        }
    time.sleep(360)