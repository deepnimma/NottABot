# Importing Libraries
from requests import get
from pathlib import Path
import os
from dotenv import load_dotenv
import Scripts.zNumberFormat
import Scripts.zSBStalk

# Loading Data From .env File
load_dotenv()
env_path = Path('.') / '.env'
api_key = os.getenv("API_KEY")

username = 'NottCurious'

# Getting UUID Using Mojang API
def getUUID(username):
	try:
		playerdata_mojang = get("https://api.mojang.com/users/profiles/minecraft/%s" % (username)).json()
	
		uuid = playerdata_mojang["id"]

		return uuid
	except:
		return 'no'

def getDungeonData(username):
	profile, profile_id = zSBStalk.getLatestProfile(getUUID(username))

	data = get('https://sky.shiiyu.moe/api/v2/profile/%s' % (username)).json()

	data = data['profiles'][profile_id]['data']['dungeons']

	pclass = data['selected_class'].capitalize()
	secretsfound = data['secrets_found']

	pages_found = data['journals']['pages_collected']
	completed_journals = data['journals']['journals_completed']

	boss_collections = [data['boss_collections']['catacombs_1']['killed'], data['boss_collections']['catacombs_2']['killed'], data['boss_collections']['catacombs_3']['killed'], data['boss_collections']['catacombs_4']['killed'], data['boss_collections']['catacombs_5']['killed'], data['boss_collections']['catacombs_6']['killed'], data['boss_collections']['catacombs_7']['killed']]

	return pclass, secretsfound, pages_found, completed_journals, boss_collections

def getFloorData(username):
	profile, profile_id = zSBStalk.getLatestProfile(getUUID(username))

	data = get('https://sky.shiiyu.moe/api/v2/profile/%s' % (username)).json()

	zdata = data['profiles'][profile_id]['data']['dungeons']['catacombs']
	data = data['profiles'][profile_id]['data']['dungeons']['catacombs']['floors']

	# entrance_data = [data[0]['best_runs'][0]['score_exploration'], data[0]['best_runs'][0]['score_speed'], data[0]['best_runs'][0]['score_skill'], data[0]['best_runs'][0]['score_bonus'], data[0]['best_runs'][0]['dungeon_class'], round(data[0]['best_runs'][0]['damage_dealt'], 2), data[0]['best_runs'][0]['deaths'], data[0]['best_runs'][0]['mobs_killed'], data[0]['best_runs'][0]['secrets_found']]
	# floor_1_data = [data[1]['best_runs'][0]['score_exploration'], data[1]['best_runs'][0]['score_speed'], data[1]['best_runs'][0]['score_skill'], data[1]['best_runs'][0]['score_bonus'], data[1]['best_runs'][0]['dungeon_class'], round(data[1]['best_runs'][0]['damage_dealt'], 2), data[1]['best_runs'][0]['deaths'], data[1]['best_runs'][0]['mobs_killed'], data[1]['best_runs'][0]['secrets_found']]
	# floor_2_data = [data[2]['best_runs'][0]['score_exploration'], data[2]['best_runs'][0]['score_speed'], data[2]['best_runs'][0]['score_skill'], data[2]['best_runs'][0]['score_bonus'], data[2]['best_runs'][0]['dungeon_class'], round(data[2]['best_runs'][0]['damage_dealt'], 2), data[2]['best_runs'][0]['deaths'], data[2]['best_runs'][0]['mobs_killed'], data[2]['best_runs'][0]['secrets_found']]
	# floor_3_data = [data[3]['best_runs'][0]['score_exploration'], data[3]['best_runs'][0]['score_speed'], data[3]['best_runs'][0]['score_skill'], data[3]['best_runs'][0]['score_bonus'], data[3]['best_runs'][0]['dungeon_class'], round(data[3]['best_runs'][0]['damage_dealt'], 2), data[3]['best_runs'][0]['deaths'], data[3]['best_runs'][0]['mobs_killed'], data[3]['best_runs'][0]['secrets_found']]
	# floor_4_data = [data[4]['best_runs'][0]['score_exploration'], data[4]['best_runs'][0]['score_speed'], data[4]['best_runs'][0]['score_skill'], data[4]['best_runs'][0]['score_bonus'], data[4]['best_runs'][0]['dungeon_class'], round(data[4]['best_runs'][0]['damage_dealt'], 2), data[4]['best_runs'][0]['deaths'], data[4]['best_runs'][0]['mobs_killed'], data[4]['best_runs'][0]['secrets_found']]
	# floor_5_data = [data[5]['best_runs'][0]['score_exploration'], data[5]['best_runs'][0]['score_speed'], data[5]['best_runs'][0]['score_skill'], data[5]['best_runs'][0]['score_bonus'], data[5]['best_runs'][0]['dungeon_class'], round(data[5]['best_runs'][0]['damage_dealt'], 2), data[5]['best_runs'][0]['deaths'], data[5]['best_runs'][0]['mobs_killed'], data[5]['best_runs'][0]['secrets_found']]
	# floor_6_data = [data[6]['best_runs'][0]['score_exploration'], data[6]['best_runs'][0]['score_speed'], data[6]['best_runs'][0]['score_skill'], data[6]['best_runs'][0]['score_bonus'], data[6]['best_runs'][0]['dungeon_class'], round(data[6]['best_runs'][0]['damage_dealt'], 2), data[6]['best_runs'][0]['deaths'], data[6]['best_runs'][0]['mobs_killed'], data[6]['best_runs'][0]['secrets_found']]
	# floor_7_data = [data[7]['best_runs'][0]['score_exploration'], data[7]['best_runs'][0]['score_speed'], data[7]['best_runs'][0]['score_skill'], data[7]['best_runs'][0]['score_bonus'], data[7]['best_runs'][0]['dungeon_class'], round(data[7]['best_runs'][0]['damage_dealt'], 2), data[7]['best_runs'][0]['deaths'], data[7]['best_runs'][0]['mobs_killed'], data[7]['best_runs'][0]['secrets_found']]

	full_data = []

	for i in data:
		full_data.append([data[i]['best_runs'][0]['score_exploration'], data[i]['best_runs'][0]['score_speed'], data[i]['best_runs'][0]['score_skill'], data[i]['best_runs'][0]['score_bonus'], data[i]['best_runs'][0]['dungeon_class'].capitalize(), zNumberFormat.comma(round(data[i]['best_runs'][0]['damage_dealt'], 2)), data[i]['best_runs'][0]['deaths'], data[i]['best_runs'][0]['mobs_killed'], data[i]['best_runs'][0]['secrets_found']])
	
	return full_data
	# return entrance_data, floor_1_data, floor_2_data, floor_3_data, floor_4_data, floor_5_data, floor_6_data, floor_7_data

def makeString(l):
	estr = ''

	estr = '```\nDungeon Class: %s\n\nExploration Score: %s\nSpeed Score: %s\nSkill Score: %s\nBonus Score: %s\n\nDamage Dealt: %s\nDeaths: %s\nMobs Killed: %s\nSecrets Found: %s\n```' % (l[4], l[0], l[1], l[2], l[3], l[5], l[6], l[7], l[8])

	return estr

# print(getFloorData('NottCurious'))