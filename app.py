from flask import Flask
from flask import render_template
from flask import request
import pickle
import numpy as np
import pandas as pd
import sklearn
import os
from collections import Counter

app = Flask(__name__)


def predict(t1, t2, map):
    files = os.listdir("Models/")
    lr = pickle.load(open("Models/" + files[0], 'rb'))
    rf = pickle.load(open("Models/" + files[1], 'rb'))
    svc = pickle.load(open("Models/" + files[2], 'rb'))
    data = pd.read_csv("Data/results1_wo_garbage_NTN.csv")

    UniqueTeams = pd.Series(np.unique(np.concatenate((data['Team1'].unique(), data['Team2'].unique()))))
    # Получаем все карты, на которых играли команды
    UniqueMaps = pd.Series(np.unique(data['Map'].unique()))

    vvod = pd.DataFrame({
        "Team1": pd.Index(UniqueTeams).get_loc(t1),
        "Team2": pd.Index(UniqueTeams).get_loc(t2),
        "Map": pd.Index(UniqueMaps).get_loc(map),
    }, index=[0])

    otvet = []
    otvet.append(str(lr.predict(vvod))[2:-2])
    otvet.append(str(rf.predict(vvod))[2:-2])
    otvet.append(str(svc.predict(vvod))[2:-2])
    c = Counter(otvet)
    ret = c.most_common(1)[0][0]

    if ret == 'Team1':
        ret = t1
    else:
        ret = t2

    return ret
    # print(lr.predict(vvod))
    # print(rf.predict(vvod))
    # print(svc.predict(vvod))


# @app.errorhandler(500)
# def error_500(error):
#     return ("Error: " + "123")


@app.route('/', methods=['post', 'get'])
def hello_world():
    data = pd.read_csv("Data/results1_wo_garbage_NTN.csv")
    if request.method == 'POST':
        # print(str(request.form.get('team1')))
        t1 = request.form.get('team1')
        t2 = request.form.get('team2')
        map = request.form.get('map')

        return render_template('index.html',
                               winner=predict(t1, t2, map),
                               teams=np.unique(np.concatenate((data['Team1'].unique(), data['Team2'].unique()))),
                               maps=np.unique(data['Map'].unique())
                               )
    else:
        return render_template('index.html',
                               teams=np.unique(np.concatenate((data['Team1'].unique(), data['Team2'].unique()))),
                               maps=np.unique(data['Map'].unique())
                               )



if __name__ == '__main__':
    app.run()
