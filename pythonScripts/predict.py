import pickle
import numpy as np
import pandas as pd
import sklearn
import os
from collections import Counter
from joblib import load

if __name__ == '__main__':
    # files = os.listdir("Models/")
    # print(files)
    # lr = pickle.load(open("Models/Logistic_regression_model.sav", 'rb'))
    rf = pickle.load(open("../Models/Random_forest.sav", 'rb'))
    # svc = pickle.load(open("Models/SVM_model.sav", 'rb'))
    # knn = pickle.load(open("Models/knn.sav", 'rb'))
    # rf1 = load("Random_forest.joblib")

    data = pd.read_csv("../Data/results8_wo_garbage_NTN.csv")

    UniqueTeams = pd.Series(np.unique(np.concatenate((data['Team1'].unique(), data['Team2'].unique()))))
    UniqueMaps = pd.Series(np.unique(data['Map'].unique()))

    # print(pd.Index(UniqueTeams).get_loc('LDLC'))
    # print(pd.Index(UniqueMaps).get_loc('Cache'))

    vvod = pd.DataFrame({
        "Team1": pd.Index(UniqueTeams).get_loc('G2'),
        "Team2": pd.Index(UniqueTeams).get_loc('Natus Vincere'),
        # 'Team1_Score': 1,
        # 'Team2_Score': 1,
        "Map": 0,
    }, index=[0])

    vvod1 = pd.DataFrame({
        "Team1": pd.Index(UniqueTeams).get_loc('Natus Vincere'),
        "Team2": pd.Index(UniqueTeams).get_loc('G2'),
        # 'Team1_Score': 1,
        # 'Team2_Score': 1,
        "Map": 0,
    }, index=[0])

    # otvet = []
    # # otvet.append(str(lr.predict(vvod))[2:-2])
    # otvet.append(str(rf.predict(vvod))[2:-2])
    # # otvet.append(str(svc.predict(vvod))[2:-2])
    # print(otvet)
    # c = Counter(otvet)
    # ret = c.most_common(1)[0][0]
    #
    # print(ret)

    # print(lr.predict(vvod1))
    # print(rf.predict(vvod1))
    # print(svc.predict(vvod1))
    #
    # print()
    # print(rf1.predict(vvod))
    # print(rf1.predict(vvod1))
    #
    #
    # print()
    # print(knn.predict(vvod))
    # print(knn.predict(vvod1))

    print("RANDOM FOREST:")
    print(rf.predict(vvod))
    print(rf.predict(vvod1))
