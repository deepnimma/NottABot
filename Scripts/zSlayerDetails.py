# Importing Libraries
from requests import get
import Scripts.zNumberFormat
from pathlib import Path
import os
from dotenv import load_dotenv


# Loading Data From .env File
load_dotenv()
env_path = Path('.') / '.env'
api_key = os.getenv("API_KEY")

def getUUID(username):
	try:
		playerdata_mojang = get("https://api.mojang.com/users/profiles/minecraft/%s" % (username)).json()
	
		uuid = playerdata_mojang["id"]

		return uuid
	except:
		return 'no'

def getLatestProfile(uuid):
	# uuid = getUUID(username)

	playerdata = get('https://api.hypixel.net/player?key=%s&uuid=%s' % (api_key, uuid)).json()

	j = 1
	latest_profile = []

	for i in playerdata['player']['stats']['SkyBlock']['profiles']:
		if j == 1:
			latest_profile = playerdata['player']['stats']['SkyBlock']['profiles'][i]['cute_name']
			latest_profile_id = playerdata['player']['stats']['SkyBlock']['profiles'][i]['profile_id']
			j += 1
	
	return latest_profile, latest_profile_id
		

def findSlayerCost(a, b, c, d):
	return a*100 + b*1000 + c*10000 + d*50000

def findSlayerLevel(exp):
	if exp > 1000000:
		return 9
	elif exp > 400000:
		return 8
	elif exp > 100000:
		return 7
	elif exp > 20000:
		return 6
	elif exp > 5000:
		return 5
	elif exp > 1000:
		return 4
	elif exp > 200:
		return 3
	elif exp > 15:
		return 2
	elif exp > 5:
		return 1
	else:
		return 0

def findCostToNextLevel(exp):
	clevel = findSlayerLevel(exp)

	if clevel == 9:
		return [0, 0, 0]

	levelreq = [0, 5, 15, 200, 1000, 5000, 20000, 100000, 400000, 1000000]

	req_exp = levelreq[clevel + 1] - exp

	t4r = req_exp / 500

	return [t4r, req_exp, t4r*50000]

def getZombieSlayerData(uuid):
	profile_name, profile_id = getLatestProfile(uuid)
	full_data = get('https://api.hypixel.net/skyblock/profile?key=%s&profile=%s' % (api_key, profile_id)).json()
	zombie_data = full_data['profile']['members'][uuid]['slayer_bosses']['zombie']

	t1_kills = zombie_data['boss_kills_tier_0']
	t2_kills = zombie_data['boss_kills_tier_1']
	t3_kills = zombie_data['boss_kills_tier_2']
	t4_kills = zombie_data['boss_kills_tier_3']

	exp = zombie_data['xp']

	level = findSlayerLevel(exp)

	moneyspent = findSlayerCost(t1_kills, t2_kills, t3_kills, t4_kills)

	t4r, req_exp, money_req = findCostToNextLevel(exp)
	
	levelcompletion = exp * 100 / (req_exp + exp)

	return [t1_kills, t2_kills, t3_kills, t4_kills, exp, level, moneyspent, levelcompletion, t4r, req_exp, numberformat.comma(money_req)]

def getSpiderSlayerData(uuid):
	profile_name, profile_id = getLatestProfile(uuid)
	full_data = get('https://api.hypixel.net/skyblock/profile?key=%s&profile=%s' % (api_key, profile_id)).json()
	zombie_data = full_data['profile']['members'][uuid]['slayer_bosses']['spider']

	t1_kills = zombie_data['boss_kills_tier_0']
	t2_kills = zombie_data['boss_kills_tier_1']
	t3_kills = zombie_data['boss_kills_tier_2']
	t4_kills = zombie_data['boss_kills_tier_3']

	exp = zombie_data['xp']

	level = findSlayerLevel(exp)

	moneyspent = findSlayerCost(t1_kills, t2_kills, t3_kills, t4_kills)

	t4r, req_exp, money_req = findCostToNextLevel(exp)
	
	levelcompletion = exp * 100 / (req_exp + exp)

	return [t1_kills, t2_kills, t3_kills, t4_kills, exp, level, moneyspent, levelcompletion, t4r, req_exp, numberformat.comma(money_req)]

def getWolfSlayerData(uuid):
	profile_name, profile_id = getLatestProfile(uuid)
	full_data = get('https://api.hypixel.net/skyblock/profile?key=%s&profile=%s' % (api_key, profile_id)).json()
	zombie_data = full_data['profile']['members'][uuid]['slayer_bosses']['wolf']

	t1_kills = zombie_data['boss_kills_tier_0']
	t2_kills = zombie_data['boss_kills_tier_1']
	t3_kills = zombie_data['boss_kills_tier_2']
	t4_kills = zombie_data['boss_kills_tier_3']

	exp = zombie_data['xp']

	level = findSlayerLevel(exp)

	moneyspent = findSlayerCost(t1_kills, t2_kills, t3_kills, t4_kills)

	t4r, req_exp, money_req = findCostToNextLevel(exp)
	
	levelcompletion = exp * 100 / (req_exp + exp)

	return [t1_kills, t2_kills, t3_kills, t4_kills, exp, level, moneyspent, levelcompletion, t4r, req_exp, numberformat.comma(money_req)]

def getExpToUp(level):
	if level == 0:
		return 5
	elif level == 1:
		return 15
	elif level == 2:
		return 200
	elif level == 3:
		return 1000
	elif level == 4:
		return 5000
	elif level == 5:
		return 20000
	elif level == 6:
		return 100000
	elif level == 7:
		return 400000
	elif level == 8:
		return 1000000
	else:
		return 1
