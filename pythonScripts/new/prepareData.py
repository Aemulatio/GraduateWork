from pymongo import MongoClient


def getPlayers() -> list:
	"""

	:return:
	"""

	players_collections = db.Players
	players = []
	for player in players_collections.find():
		players.append(player)
	return players


def getStats():
	stats_collection = db.Stats
	players_collections = db.Players
	for stat in stats_collection.find().sort("current_team"):
		team1_len = players_collections.count_documents({'current_team': stat['team1']})
		team2_len = players_collections.count_documents({'current_team': stat['team2']})
		if team1_len > 0 and team2_len > 0:
			t1_rating = 0
			t1_dpr = 0
			t1_kast = 0
			t1_impact = 0
			t1_adr = 0
			t1_kpr = 0
			for team1_obj in players_collections.find({'current_team': stat['team1']}):
				t1_rating += team1_obj['rating']
				t1_dpr += team1_obj['dpr']
				t1_kast += team1_obj['kast']
				t1_impact += team1_obj['impact']
				t1_adr += team1_obj['adr']
				t1_kpr += team1_obj['kpr']

			t2_rating = 0
			t2_dpr = 0
			t2_kast = 0
			t2_impact = 0
			t2_adr = 0
			t2_kpr = 0
			for team2_obj in players_collections.find({'current_team': stat['team2']}):
				t2_rating += team2_obj['rating']
				t2_dpr += team2_obj['dpr']
				t2_kast += team2_obj['kast']
				t2_impact += team2_obj['impact']
				t2_adr += team2_obj['adr']
				t2_kpr += team2_obj['kpr']
			
			print("-------------------")

	# print(stat['team1'])
	# for player in players_collections.find({'current_team': stat['team1']}):
	# 	print(player)


if __name__ == '__main__':
	client = MongoClient(
		"mongodb+srv://new:oIGh34Xd8010lrgj@cluster0.rg6wi.mongodb.net/Cluster0?retryWrites=true&w=majority")
	db = client.Diploma
	# allPlayers = getPlayers()
	# print(allPlayers)
	getStats()
