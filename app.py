import base64

from flask import Flask
from flask import render_template
from flask import request
import pickle
import numpy as np
import pandas as pd
import os
from sklearn.model_selection import train_test_split
from sklearn import ensemble
from pymongo import MongoClient
import json

app = Flask(__name__)


def predict(t1, t2, game_map):
    if "RANDOM_FOREST.pickle" not in os.listdir("Models/"):
        model = pickle.load(open("Models/SVM_model.sav", 'rb'))
    else:
        model = pickle.load(open("Models/RANDOM_FOREST.pickle", 'rb'))
    data = pd.read_csv("Data/results6_wo_garbage_NTN.csv")
    # print(data)
    UniqueTeams = pd.Series(np.unique(np.concatenate((data['Team1'].unique(), data['Team2'].unique()))))
    # Получаем все карты, на которых играли команды
    UniqueMaps = pd.Series(np.unique(data['Map'].unique()))

    vvod = pd.DataFrame({
        "Team1": pd.Index(UniqueTeams).get_loc(t1),
        "Team2": pd.Index(UniqueTeams).get_loc(t2),
        "Map": pd.Index(UniqueMaps).get_loc(game_map),
    }, index=[0])

    ret = model.predict(vvod)
    if ret == 'Team1':
        ret = t1
    else:
        ret = t2

    del vvod, UniqueTeams, UniqueMaps, model
    return ret


def getLogs():
    client = MongoClient(
        "mongodb+srv://new:oIGh34Xd8010lrgj@cluster0.rg6wi.mongodb.net/Cluster0?retryWrites=true&w=majority")
    db = client.Diploma
    collection = db.logs
    data = []
    for obj in collection.find():
        data.append(obj['date'].strftime("%d.%m.%Y, %H:%M:%S"))
    return data


def getTeams():
    client = MongoClient(
        "mongodb+srv://new:oIGh34Xd8010lrgj@cluster0.rg6wi.mongodb.net/Cluster0?retryWrites=true&w=majority")
    db = client.Diploma
    collection = db.Teams
    data = []
    for obj in collection.find().sort('teamName'):
        object = {
            'teamName': obj['teamName'],
            'teamUrl': obj[obj['teamName']]['teamUrl'],
            'teamLogo': base64.b64decode(obj[obj['teamName']]['teamLogo']).decode('utf-8'),
            'player1': obj[obj['teamName']]['player1'],
            'player2': obj[obj['teamName']]['player2'],
            'player3': obj[obj['teamName']]['player3'],
            'player4': obj[obj['teamName']]['player4'],
            'player5': obj[obj['teamName']]['player5'],

        }
        data.append(object)
    return data


@app.errorhandler(500)
def error_500(error):
    print(request.form)
    print(request.method)
    return error


@app.errorhandler(404)
def error_500(error):
    print(request.form)
    print(request.method)
    print(error)
    return render_template("404.html")


def train_forest():
    data = pd.read_csv("Data/results6_wo_garbage_NTN.csv")
    UniqueTeams = pd.Series(np.unique(np.concatenate((data['Team1'].unique(), data['Team2'].unique()))))
    # Получаем все карты, на которых играли команды
    UniqueMaps = pd.Series(np.unique(data['Map'].unique()))
    data = data.drop(['Team1_Score', 'Team2_Score'], 1)
    print("TRAIN")
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
@app.route('/index.html', methods=['post', 'get'])
def main():
    data = pd.read_csv("Data/results6_wo_garbage_NTN.csv")
    #     logos = os.listdir("static/imgs/logos")
    #     teams =
    if "RANDOM_FOREST.pickle" not in os.listdir("Models/"):
        train_forest()
    if request.method == 'POST':
        # print(str(request.form.get('team1')))
        t1 = request.form.get('team1')
        t2 = request.form.get('team2')
        game_map = request.form.get('map')

        print(t1, t2, game_map)

        return render_template('index.html',
                               winner=predict(t1, t2, game_map),
                               teams=np.unique(np.concatenate((data['Team1'].unique(), data['Team2'].unique()))),
                               maps=np.unique(data['Map'].unique()),
                               team1=t1,
                               team2=t2,
                               map=map,
                               new_teams=getTeams()
                               )
    else:
        return render_template('index.html',
                               teams=np.unique(np.concatenate((data['Team1'].unique(), data['Team2'].unique()))),
                               maps=np.unique(data['Map'].unique()),
                               new_teams=getTeams(),
                               )


@app.route('/test.html', methods=['post', 'get'])
def test():
    data = pd.read_csv("Data/results6_wo_garbage_NTN.csv")
    if "RANDOM_FOREST.pickle" not in os.listdir("Models/"):
        train_forest()
    if request.method == 'POST':
        # print(str(request.form.get('team1')))
        t1 = request.form.get('team1')
        t2 = request.form.get('team2')
        map = request.form.get('map')

        return render_template('test.html',
                               winner=predict(t1, t2, map),
                               teams=np.unique(np.concatenate((data['Team1'].unique(), data['Team2'].unique()))),
                               maps=np.unique(data['Map'].unique()),
                               team1=t1,
                               team2=t2,
                               map=map
                               )
    else:
        return render_template('test.html',
                               teams=np.unique(np.concatenate((data['Team1'].unique(), data['Team2'].unique()))),
                               maps=np.unique(data['Map'].unique())
                               )


@app.route("/statistics.html")
@app.route("/statistics/")
@app.route("/statistics")
def statistics():
    last_update = getLogs()
    return render_template("statistics.html",
                           last_update=last_update)


if __name__ == '__main__':
    app.run(debug=True)
