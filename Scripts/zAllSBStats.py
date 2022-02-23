# Importing Libraries
from requests import get
print('[Scripts.zAllSBStats] - Imported requests.get')

from pathlib import Path
print('[Scripts.zAllSBStats] - Imported pathlib.Path')

import os
print('[Scripts.zAllSBStats] - Imported os')

from dotenv import load_dotenv
print('[Scripts.zAllSBStats] - Imported dotenv.load_dotenv')

import zNumberFormat
print('[Scripts.zAllSBStats] - Imported Scripts.zNumberFormat')

import zSBStalk
print('[Scripts.zAllSBStats] - Imported Scripts.zSBStalk')


# Loading Data From .env File
load_dotenv()
env_path = Path('.') / '.env'
api_key = os.getenv("API_KEY")
print('[Scripts.zAllSBStats] - Read API_Key from ENV')

# Getting UUID Using Mojang API
def getUUID(username):
	try:
		playerdata_mojang = get("https://api.mojang.com/users/profiles/minecraft/%s" % (username)).json()
		print('[Scripts.zAllSBStats.getUUID] - Mojang API Response Positive')

		uuid = playerdata_mojang["id"]
		print('[Scripts.zAllSBStats.getUUID] - Returning UUID')

		return uuid
	except:
		print('[Scripts.zAllSBStats.getUUID] - Error, Can\'t Return UUID, Exiting')
		return 'no'

# 	print('[Scripts.zAllSBStats] - ')

def getLatestProfile(username):
	print('[Scripts.zAllSBStats.getLatestProfile] - Calling Scripts.zSBStalk.getLatestProfile')
	print('[Scripts.zAllSBStats.getLatestProfile] - Returning Profile')
	return zSBStalk.getLatestProfile(getUUID(username))

def getStats(username):
	print('[Scripts.zAllSBStats.getStats] - Getting Profile Data')
	latestProfile, latestProfileID = getLatestProfile(username)
	print('[Scripts.zAllSBStats.getStats] - Received Profile Data')


	data = get('https://sky.shiiyu.moe/api/v2/profile/%s' % (username)).json()['profiles'][latestProfileID]['data']['stats']
	print('[Scripts.zAllSBStats.getStats] - Receiving Data from API with username: %s' % (username))

	print('[Scripts.zAllSBStats.getStats] - Parsing JSON File')
	health = zNumberFormat.comma(data['health'])
	defence = zNumberFormat.comma(data['defense'])
	effective_health = zNumberFormat.comma(data['effective_health'])
	strength = zNumberFormat.comma(data['strength'])
	speed = zNumberFormat.comma(data['speed'])
	intelligence = zNumberFormat.comma(data['intelligence'])
	sea_creature_chance = zNumberFormat.comma(data['sea_creature_chance'])
	magic_find = zNumberFormat.comma(data['magic_find'])
	pet_luck = zNumberFormat.comma(data['pet_luck'])
	ferocity = zNumberFormat.comma(data['ferocity'])
	ability_damage = zNumberFormat.comma(data['ability_damage'])
	mining_speed = zNumberFormat.comma(data['mining_speed'])
	mining_fortune = zNumberFormat.comma(data['mining_fortune'])
	farming_fortune = zNumberFormat.comma(data['farming_fortune'])
	foraging_fortune = zNumberFormat.comma(data['foraging_fortune'])
	print('[Scripts.zAllSBStats.getStats] - JSON File Parsed, Values Stored')

	talismans = get('https://sky.shiiyu.moe/api/v2/profile/%s' % (username)).json()['profiles'][latestProfileID]['data']['talismanCount']
	print('[Scripts.zAllSBStats.getStats] - Receiving Talisman Data')

	print('[Scripts.zAllSBStats.getStats] - Returning All Data')
	return [health, defence, effective_health, strength, speed, intelligence, sea_creature_chance, magic_find, pet_luck, ferocity, ability_damage, mining_speed, mining_fortune, farming_fortune, foraging_fortune]

def getFairySouls(username):
	print('[Scripts.zAllSBStats.getFairySouls] - Getting Profile Data')
	latestProfile, latestProfileID = getLatestProfile(username)
	print('[Scripts.zAllSBStats.getFairySouls] - Received Profile Data')

	data = get('https://sky.shiiyu.moe/api/v2/profile/%s' % (username)).json()['profiles'][latestProfileID]['data']['fairy_souls']
	print('[Scripts.zAllSBStats.getFairySouls] - Receiving Fairy Souls Data')

	print('[Scripts.zAllSBStats.getFairySouls] - Parsing Data')
	collected = data['collected']
	total = data['total']
	progress = round(data['progress'] * 100, 2)
	print('[Scripts.zAllSBStats.getFairySouls] - Data Parsing Complete')

	print('[Scripts.zAllSBStats.getFairySouls] - Returning Values')
	return [collected, total, progress]
	
def maincommand(username):
	stats = getStats(username)
	fairy_souls = getFairySouls(username)

	return stats + fairy_souls

maincommand('nottcurious')