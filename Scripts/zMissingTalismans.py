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

# username = 'NottCurious'

# Getting UUID Using Mojang API
def getUUID(username):
	try:
		playerdata_mojang = get("https://api.mojang.com/users/profiles/minecraft/%s" % (username)).json()
	
		uuid = playerdata_mojang["id"]

		return uuid
	except:
		return 'no'

def getMissingTalismans(username):
	missing_talismans = []

	latest_profile, latest_profile_id = zSBStalk.getLatestProfile(getUUID(username))

	data = get('https://sky.shiiyu.moe/api/v2/profile/%s' % (username)).json()
	data = data['profiles'][latest_profile_id]['data']['missingTalismans']

	for i in range(len(data)):
		tali = data[i]['display_name']
		if tali == 'Beastmaster Crest':
			tali = tali + ' ' + data[i]['rarity'].capitalize()

		missing_talismans.append(tali)

	return missing_talismans

