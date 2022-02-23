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

def getPets(username):
	profile, profile_id = zSBStalk.getLatestProfile(getUUID(username))

	data = get('https://sky.shiiyu.moe/api/v2/profile/%s' % (username)).json()

	data = data['profiles'][profile_id]['data']['pets']

	pets = []

	for i in data:
		pets.append(i['rarity'].capitalize() + ' ' + i['display_name'].capitalize() + ' Level ' + str(i['level']['level']))

	return pets


def getMissingPets(username):
	profile, profile_id = zSBStalk.getLatestProfile(getUUID(username))

	data = get('https://sky.shiiyu.moe/api/v2/profile/%s' % (username)).json()

	data = data['profiles'][profile_id]['data']['missingPets']

	pets = []

	for i in data:
		pets.append(i['display_name'].capitalize())

	return pets

