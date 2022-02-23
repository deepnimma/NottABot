# Importing Libraries
from requests import get
from pathlib import Path
import os
from dotenv import load_dotenv
import Scripts.zNumberFormat

# Loading Data From .env File
load_dotenv()
env_path = Path('.') / '.env'
api_key = os.getenv("API_KEY")

# username = 'NottCurious'

# Getting UUID Using Mojang API
def getUUID(username):
	try:
		playerdata_mojang = get("https://api.mojang.com/users/profiles/minecraft/%s" % (username)).json()
	
		uuid = playerdata_mojang["id"]

		return uuid
	except:
		return 'no'

def getProfileCuteNames(uuid):
	profs = []
	playerdata = get('https://api.hypixel.net/player?key=%s&uuid=%s' % (api_key, uuid)).json()
	for i in playerdata['player']['stats']['SkyBlock']['profiles']:
		profs.append(i)

	return profs	

def getProfiles(uuid):
	profs = []
	playerdata = get('https://api.hypixel.net/player?key=%s&uuid=%s' % (api_key, uuid)).json()
	for i in playerdata['player']['stats']['SkyBlock']['profiles']:
		profs.append(playerdata['player']['stats']['SkyBlock']['profiles'][i]['cute_name'])

	return profs

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


def getBankBalance(uuid):
	profile_name, profile_id = getLatestProfile(uuid)
	sbdata = get('https://api.hypixel.net/skyblock/profile?key=%s&profile=%s' % (api_key, profile_id)).json()


	try:
		bank_money = sbdata['profile']['banking']['balance']
		purse = sbdata['profile']['members'][uuid]['coin_purse']
	except:
		return 'no', 'no'

	return round(bank_money, 2), round(purse, 2)

def formatExp(exp):
	exptoup = [0, 50, 125, 200, 300, 500, 750, 1000, 1500, 2000, 3500, 5000, 7500, 10000, 15000, 20000, 30000, 50000, 75000, 100000, 200000, 300000, 400000, 500000, 600000, 700000, 800000, 900000, 1000000, 1100000, 1200000, 1300000, 1400000, 1500000, 1600000, 1700000, 1800000, 1900000, 2000000, 2100000, 2200000, 2300000, 2400000, 2500000, 2600000, 2750000, 2900000, 3100000, 3400000, 3700000, 4000000, 4300000, 4600000, 4900000, 5200000, 5500000, 5800000, 6100000, 6400000, 6700000, 7000000] 

	i = 0

	while exp >= exptoup[i] and i in range(len(exptoup) - 1):
		exp -= exptoup[i]
		i += 1

	return (i if i == 60 else i - 1), exp, exptoup[i]

def getSkills(uuid):
	profile_name, profile_id = getLatestProfile(uuid)
	sbdata = get('https://api.hypixel.net/skyblock/profile?key=%s&profile=%s' % (api_key, profile_id)).json()


	datap = sbdata['profile']['members'][uuid]

	combat, combatexp, combattoup = formatExp(round(datap['experience_skill_combat'], 2))
	foraging, foragingexp, foragingtoup = formatExp(round(datap['experience_skill_foraging'], 2))
	farming, farmingexp, farmingtoup = formatExp(round(datap['experience_skill_farming'], 2))
	enchanting, enchantingexp, enchantingtoup = formatExp(round(datap['experience_skill_enchanting'], 2))
	alchemy, alchemyexp, alchemytoup = formatExp(round(datap['experience_skill_alchemy'], 2))
	mining, miningexp, miningtoup = formatExp(round(datap['experience_skill_mining'], 2))
	fishing, fishingexp, fishingtoup = formatExp(round(datap['experience_skill_fishing'], 2))

	return [combat, foraging, farming, enchanting, alchemy, mining, fishing], [combatexp, foragingexp, farmingexp, enchantingexp, alchemyexp, miningexp, fishingexp], [combattoup, foragingtoup, farmingtoup, enchantingtoup, alchemytoup, miningtoup, fishingtoup]

def findSkillAverage(uuid):
	p, c, d= getSkills(uuid)

	sum = 0

	for i in p:
		sum += i

	return round(sum / 7, 2)


