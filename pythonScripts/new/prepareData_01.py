from pymongo import MongoClient
from db import connectionString


def getStats():
    stats_collection = db.Stats
    players_collections = db.Players
    prepareData_collection = db.Prepare_01
    prepareData_collection.drop()
    for stat in stats_collection.find().sort("current_team"):
        team1_len = players_collections.count_documents({'current_team': stat['team1']})
        team2_len = players_collections.count_documents({'current_team': stat['team2']})
        if team1_len > 0 and team2_len > 0:
            print(stat)
            t1_rating = 0
            t1_dpr = 0
            t1_kast = 0
            t1_impact = 0
            t1_adr = 0
            t1_kpr = 0
            for team1_obj in players_collections.find({'current_team': stat['team1']}):
                t1_rating += float(team1_obj['rating'])
                t1_dpr += float(team1_obj['dpr'])
                t1_kast += float(team1_obj['kast'].replace("%", ''))
                t1_impact += float(team1_obj['impact'])
                t1_adr += float(team1_obj['adr'])
                t1_kpr += float(team1_obj['kpr'])

            t2_rating = 0
            t2_dpr = 0
            t2_kast = 0
            t2_impact = 0
            t2_adr = 0
            t2_kpr = 0
            for team2_obj in players_collections.find({'current_team': stat['team2']}):
                t2_rating += float(team2_obj['rating'])
                t2_dpr += float(team2_obj['dpr'])
                t2_kast += float(team2_obj['kast'].replace("%", ''))
                t2_impact += float(team2_obj['impact'])
                t2_adr += float(team2_obj['adr'])
                t2_kpr += float(team2_obj['kpr'])

            if stat['winner'] == stat['team1']:
                winner = 0
            else:
                winner = 1

            prepareData_collection.insert_one({
                'winner': winner,
                "t1_rating": round(t1_rating / team1_len, 3),
                't1_dpr': round(t1_dpr / team1_len, 3),
                't1_kast': round(t1_kast / team1_len, 3),
                't1_impact': round(t1_impact / team1_len, 3),
                't1_adr': round(t1_adr / team1_len, 3),
                't1_kpr': round(t1_kpr / team1_len, 3),
                "t2_rating": round(t2_rating / team2_len, 3),
                't2_dpr': round(t2_dpr / team2_len, 3),
                't2_kast': round(t2_kast / team2_len, 3),
                't2_impact': round(t2_impact / team2_len, 3),
                't2_adr': round(t2_adr / team2_len, 3),
                't2_kpr': round(t2_kpr / team2_len, 3),
            })
            print("-------------------")


if __name__ == '__main__':
    client = MongoClient(connectionString)
    db = client.Diploma
    getStats()
