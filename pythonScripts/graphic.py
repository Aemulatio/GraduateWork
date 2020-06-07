import numpy as np
import pandas as pd
import json
from collections import defaultdict

data = pd.read_csv('../Data/results5_wo_garbage_TN.csv')
UniqueTeams = pd.Series(np.unique(np.concatenate((data['Team1'].unique(), data['Team2'].unique()))))
UniqueMaps = pd.Series(np.unique(data['Map'].unique()))

for team in UniqueTeams:
    matches = defaultdict(int)
    wins = defaultdict(int)
    for row in data.values:
        if team in row:
            matches[row[-1]] += 1
            if team == row[0]:
                wins[row[-1]] += 1
    for map in UniqueMaps:
        if map not in matches.keys():
            matches[map] = 0
        if map not in wins.keys():
            wins[map] = 0

    if '\\t' in team:
        team = team.replace('\\t', '')
    with open("../static/jsons/" + team.strip() + "_wins.json", "w") as write_file:
        json.dump(wins, write_file)
    with open("../static/jsons/" + team.strip() + "_matches.json", "w") as write_file:
        json.dump(matches, write_file)
    # print(json.dumps(result))
    # print(matches)
    # print(wins)
    # print(team)
