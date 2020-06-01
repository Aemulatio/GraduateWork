import pickle
import numpy as np
import pandas as pd
import sklearn
import os

if __name__ == '__main__':
    files = os.listdir("Models/pickle/")
    lr = pickle.load(open("Models/pickle/" + files[0], 'rb'))
    rf = pickle.load(open("Models/pickle/" + files[1], 'rb'))
    svc = pickle.load(open("Models/pickle/" + files[2], 'rb'))

    vvod = pd.DataFrame({
        "Team1": 25,
        "Team2": 72,
        "Map": 5,
    }, index=[0])

    print(lr.predict(vvod))
    print(rf.predict(vvod))
    print(svc.predict(vvod))
