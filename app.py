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

import requests
from bs4 import BeautifulSoup

app = Flask(__name__)


def getPlayerCurrentMapStats(url: str, mapname: str):
    url += "?maps=de_" + mapname.lower()
    print(url)
    r = requests.get(url, headers=headers)
    if r.status_code == 200:  # 200 - ok
        html = r.text  # код текущей страницы в переменную
        soup = BeautifulSoup(html, features='html.parser')  # объект BS
        stats = soup.select("div.summaryStatBreakdownDataValue")
        rating = float(stats[0].get_text())
        dpr = float(stats[1].get_text())
        kast = float(stats[2].get_text().replace("%", ""))
        impact = float(stats[3].get_text())
        adr = float(stats[4].get_text())
        kpr = float(stats[5].get_text())
        return rating, dpr, kast, impact, adr, kpr
    else:
        return OSError


def getTeamStats(teamname: str, mapname: str):
    """

    :return:
    """
    collection = db.Teams
    rating = 0
    dpr = 0
    kast = 0
    impact = 0
    adr = 0
    kpr = 0
    for obj in collection.find({'teamName': teamname}):
        p1 = obj[teamname]['player1']['url'].replace("/player/", "/stats/players/")
        temp = getPlayerCurrentMapStats(p1, mapname)
        rating += temp[0]
        dpr += temp[1]
        kast += temp[2]
        impact += temp[3]
        adr += temp[4]
        kpr += temp[5]
        p2 = obj[teamname]['player2']['url'].replace("/player/", "/stats/players/")
        temp = getPlayerCurrentMapStats(p2, mapname)
        rating += temp[0]
        dpr += temp[1]
        kast += temp[2]
        impact += temp[3]
        adr += temp[4]
        kpr += temp[5]
        p3 = obj[teamname]['player3']['url'].replace("/player/", "/stats/players/")
        temp = getPlayerCurrentMapStats(p3, mapname)
        rating += temp[0]
        dpr += temp[1]
        kast += temp[2]
        impact += temp[3]
        adr += temp[4]
        kpr += temp[5]
        p4 = obj[teamname]['player4']['url'].replace("/player/", "/stats/players/")
        temp = getPlayerCurrentMapStats(p4, mapname)
        rating += temp[0]
        dpr += temp[1]
        kast += temp[2]
        impact += temp[3]
        adr += temp[4]
        kpr += temp[5]
        p5 = obj[teamname]['player5']['url'].replace("/player/", "/stats/players/")
        temp = getPlayerCurrentMapStats(p5, mapname)
        rating += temp[0]
        dpr += temp[1]
        kast += temp[2]
        impact += temp[3]
        adr += temp[4]
        kpr += temp[5]
        rating /= 5
        dpr /= 5
        kast /= 5
        impact /= 5
        adr /= 5
        kpr /= 5
        return teamname + " " + str(round(rating, 3)) + " " + str(round(dpr, 3)) + " " + \
               str(round(kast, 3)) + " " + str(round(impact, 3)) + " " + str(round(adr, 3)) + " " + str(round(kpr, 3))


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


def new_predict(t1, t2, map):
    team1 = getTeamStats(t1, map)
    team2 = getTeamStats(t2, map)
    print(team1)
    print(team2)

    # data = pd.DataFrame({
    #     'Team1': team1,
    #     'Team2': team2,
    # }, index=[0])


def getLogs():
    collection = db.logs
    data = []
    for obj in collection.find():
        data.append(obj['date'].strftime("%d.%m.%Y, %H:%M:%S"))
    return data


def getTeams():
    collection = db.Teams
    data = []
    for obj in collection.find().sort('teamName'):
        object = {
            'teamName': obj['teamName'],
            'teamUrl': obj[obj['teamName']]['teamUrl'],
            'teamLogo': obj[obj['teamName']]['teamLogo'],
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
def error_404(error):
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


@app.route('/test', methods=['post', 'get'])
@app.route('/test/', methods=['post', 'get'])
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
    client = MongoClient(
        "mongodb+srv://new:oIGh34Xd8010lrgj@cluster0.rg6wi.mongodb.net/Cluster0?retryWrites=true&w=majority")
    db = client.Diploma
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36",
        "pragma": 'no-cache',
        "cache-control": "no-cache",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "cookie": "CookieConsent={stamp:%27/iFeOz/wnfocVsfOloyCZGDBUppd7M6E1eceKMjQySF6mGHlsx+DGg==%27%2Cnecessary:true%2Cpreferences:true%2Cstatistics:true%2Cmarketing:true%2Cver:1%2Cutc:1616914016722%2Cregion:%27ru%27}; _ga=GA1.2.36646224.1634998534; _gid=GA1.2.2001879148.1634998534; MatchFilter={%22active%22:false%2C%22live%22:false%2C%22stars%22:1%2C%22lan%22:false%2C%22teams%22:[]}; _pbjs_userid_consent_data=6683316680106290; _lr_geo_location=RU; _lr_env_src_ats=false; pbjs-unifiedid=%7B%22TDID%22%3A%22d2047997-ef87-4ba1-bed6-b251a4919cab%22%2C%22TDID_LOOKUP%22%3A%22TRUE%22%2C%22TDID_CREATED_AT%22%3A%222021-09-23T14%3A15%3A39%22%7D; sharedid=%7B%22id%22%3A%2201FJPR3NAQRENC21NTC8NPJ478%22%2C%22ts%22%3A1634998538926%7D; cto_bundle=zToV4l9uR2xMZlhsRG95ZSUyRkxVTUg5a01Ha0M2SyUyRm4ySmVzTHFKYzNocVFzcHFRU0lRNVliSEhrWWNXc2FQNldvcUNiWHVkVkdPc2FOSXBRc2JLZWFxRVNQWVltVHByUktETTh1YTdBU1I2ODh1MWRUaUJjbG5WJTJGZm1Kc0dDMkM0MmZmUk9QRE10NyUyRlE2NnglMkZpQ3o2ZjdlOSUyRmclM0QlM0Q; _ia__v4=%7B%22v%22%3A3%2C%22r%22%3A%22RU%22%2C%22sportsbook%22%3A%5B0%2C1%5D%7D; pbjs-id5id=%7B%22created_at%22%3A%222021-10-23T14%3A15%3A33Z%22%2C%22id5_consent%22%3Atrue%2C%22original_uid%22%3A%22ID5*rGk8vAlFomWD2PVavpahlzmh0B5vsoNiGC51qQspJqYAAAh3_mOmco5vwuApR3VG%22%2C%22universal_uid%22%3A%22ID5*Hf1nsQVBi-AOQNFLAijbPfC0doYJAyPQgDolhiSFTJcAAF2WidzBTU2HuAAaWPJu%22%2C%22signature%22%3A%22ID5_Abe7-LsG5eqPJjeERPs1m6bkEGXRwEPl3M1muPSevaednZHtjcc106J6mG7SbD1H61VMe0Ebx3G5KJ5fG0vxCGg%22%2C%22link_type%22%3A2%2C%22cascade_needed%22%3Atrue%2C%22privacy%22%3A%7B%22jurisdiction%22%3A%22other%22%2C%22id5_consent%22%3Atrue%7D%7D; pbjs-id5id_last=Sun%2C%2024%20Oct%202021%2007%3A29%3A42%20GMT; _lr_retry_request=true; _gat=1; outbrain_cid_fetch=true"
    }
    # new_predict('K23', 'fnatic', 'Nuke')
    app.run(debug=True)
