from pymongo import MongoClient
import json


def setTeams(input_file: str):
    client = MongoClient(
        "mongodb+srv://new:oIGh34Xd8010lrgj@cluster0.rg6wi.mongodb.net/Cluster0?retryWrites=true&w=majority")
    db = client.Diploma
    collection = db.Teams
    f = open(input_file, 'r', encoding='utf-8')
    data = json.loads(f.read())
    for row in data.items():
        collection.insert_one({"teamName": row[0],
                               row[0]: row[1]})


if __name__ == '__main__':
    setTeams("../Data/New/teams.json")
