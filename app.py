from flask import Flask
from flask import render_template
from flask import request
import pickle
import numpy as np
import pandas as pd
import sklearn
import os
from collections import Counter
from joblib import load

app = Flask(__name__)


def predict(t1, t2, map):
    if "RANDOM_FOREST.pickle" not in os.listdir("Models/"):
        model = pickle.load(open("Models/SVM_model.sav", 'rb'))
    else:
        model = pickle.load(open("Models/RANDOM_FOREST.pickle", 'rb'))
    data = pd.read_csv("Data/results1_wo_garbage_NTN.csv")

    UniqueTeams = pd.Series(np.unique(np.concatenate((data['Team1'].unique(), data['Team2'].unique()))))
    # Получаем все карты, на которых играли команды
    UniqueMaps = pd.Series(np.unique(data['Map'].unique()))

    vvod = pd.DataFrame({
        "Team1": pd.Index(UniqueTeams).get_loc(t1),
        "Team2": pd.Index(UniqueTeams).get_loc(t2),
        "Map": pd.Index(UniqueMaps).get_loc(map),
    }, index=[0])

    ret = model.predict(vvod)
    if ret == 'Team1':
        ret = t1
    else:
        ret = t2

    del vvod
    del UniqueTeams
    del UniqueMaps
    del model
    return ret


@app.errorhandler(500)
def error_500(error):
    return (error)


from sklearn.model_selection import train_test_split
from sklearn import ensemble


def train_forest():
    data = pd.read_csv("Data/results1_wo_garbage_NTN.csv")
    UniqueTeams = pd.Series(np.unique(np.concatenate((data['Team1'].unique(), data['Team2'].unique()))))
    # Получаем все карты, на которых играли команды
    UniqueMaps = pd.Series(np.unique(data['Map'].unique()))
    data = data.drop(['Team1_Score', 'Team2_Score'], 1)

    X_all = data.drop(['Winner'], 1)
    y_all = data['Winner']

    for id, team in UniqueTeams.items():
        X_all = X_all.replace(team, id)
    for id, map in UniqueMaps.items():
        X_all = X_all.replace(map, id)

    X_train, X_test, y_train, y_test = train_test_split(X_all, y_all,
                                                        test_size=0.28,
                                                        random_state=42, )

    rf = ensemble.RandomForestClassifier(n_estimators=170, random_state=11)
    rf.fit(X_train, y_train)
    pickle.dump(rf, open("Models/RANDOM_FOREST.pickle", 'wb'))
    del rf, X_test, X_train, y_train, y_test, data


@app.route('/', methods=['post', 'get'])
def main():
    data = pd.read_csv("Data/results1_wo_garbage_NTN.csv")
    if "RANDOM_FOREST.pickle" not in os.listdir("Models/"):
        train_forest()
    if request.method == 'POST':
        # print(str(request.form.get('team1')))
        t1 = request.form.get('team1')
        t2 = request.form.get('team2')
        map = request.form.get('map')

        return render_template('index.html',
                               winner=predict(t1, t2, map),
                               teams=np.unique(np.concatenate((data['Team1'].unique(), data['Team2'].unique())))[1:],
                               maps=np.unique(data['Map'].unique()),
                               team1=t1,
                               team2=t2,
                               map=map
                               )
    else:
        return render_template('index.html',
                               teams=np.unique(np.concatenate((data['Team1'].unique(), data['Team2'].unique())))[1:],
                               maps=np.unique(data['Map'].unique())
                               )


if __name__ == '__main__':
    app.run()
