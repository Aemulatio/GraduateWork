from pymongo import MongoClient
import json


def setTeams(input_file: str):
    # client = MongoClient(
    #     "mongodb+srv://new:oIGh34Xd8010lrgj@cluster0.rg6wi.mongodb.net/Cluster0?retryWrites=true&w=majority")
    # db = client.Diploma
    collection = db.Teams
    for obj in collection.find():
        collection.delete_many(obj)
    f = open(input_file, 'r', encoding='utf-8')
    data = json.loads(f.read())
    # print(data)
    for row in data:  # .items():
        print(row)
        # collection.insert_one({"teamName": row[0],
        #                        row[0]: row[1]})
        collection.insert_one({"teamName": row.get('teamName'),
                               row.get('teamName'): row.get(row.get('teamName'))})


def setMaps(input_file: str):
    collection = db.Maps
    for obj in collection.find():
        collection.delete_many(obj)
    f = open(input_file, 'r', encoding='utf-8')
    data = json.loads(f.read())
    for row in data.items():
        collection.insert_one(row[1])
        # print(row[1])


def setStats(input_file: str):
    collection = db.Stats
    f = open(input_file, 'r', encoding='utf-8')
    data = json.loads(f.read())
    for row in data.items():
        collection.insert_one(
            {"winner": row[0],
             "team1": row[1],
             "team1_p1": row[2],
             "team1_p2": row[3],
             "team1_p3": row[4],
             "team1_p4": row[5],
             "team1_p5": row[6],
             "team2": row[7],
             "team2_p1": row[8],
             "team2_p2": row[9],
             "team2_p3": row[10],
             "team2_p4": row[11],
             "team2_p5": row[12],
             "map": row[13]})
        # print(row[1])


if __name__ == '__main__':
    client = MongoClient(
        "mongodb+srv://new:oIGh34Xd8010lrgj@cluster0.rg6wi.mongodb.net/Cluster0?retryWrites=true&w=majority")
    db = client.Diploma
    # setTeams("../Data/New/teams.json")
    # setTeams("../Data/New/teams_from_db_with_logos.json")
    # setMaps("../Data/New/maps.json")
    setStats()
