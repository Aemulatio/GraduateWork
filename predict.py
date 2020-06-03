import pickle
import numpy as np
import pandas as pd
import sklearn
import os
from collections import Counter

if __name__ == '__main__':
    files = os.listdir("Models/")
    lr = pickle.load(open("Models/" + files[0], 'rb'))
    rf = pickle.load(open("Models/" + files[1], 'rb'))
    svc = pickle.load(open("Models/" + files[2], 'rb'))

    vvod = pd.DataFrame({
        "Team1": 25,
        "Team2": 72,
        "Map": 5,
    }, index=[0])

    vvod1 = pd.DataFrame({
        "Team1": 72,
        "Team2": 25,
        "Map": 5,
    }, index=[0])

    otvet = []
    otvet.append(str(lr.predict(vvod))[2:-2])
    otvet.append(str(rf.predict(vvod))[2:-2])
    otvet.append(str(svc.predict(vvod))[2:-2])
    print(otvet)
    c = Counter(otvet)
    ret = c.most_common(1)[0][0]

    print(ret)

    print(lr.predict(vvod1))
    print(rf.predict(vvod1))
    print(svc.predict(vvod1))
