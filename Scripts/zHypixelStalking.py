# Importing Libraries
from requests import get
from pathlib import Path
import os
from dotenv import load_dotenv

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

# Checking Whether Player Is Currently Online on Hypixel Server
def check_status(uuid):
	playerdata_status = get("https://api.hypixel.net/status?key=%s&uuid=%s" % (api_key, uuid)).json()

	
	return playerdata_status['session']['online']

# Changing API Value to 'Online'/'Offline'
def format_status(uuid):
	status = check_status(uuid)

	if status == False:
		return 'Offline'
	else:
		return 'Online'

# Getting Guild of Player
def get_guild(uuid):
	playerdata_guild = get('https://api.hypixel.net/guild?key=%s&player=%s' % (api_key, uuid)).json()

	# If Player Guild Exists Return Guild Name, Otherwise Return 'No Guild'
	if playerdata_guild['guild'] == None:
		return 'No Guild'

	guild_name = playerdata_guild['guild']['name']
	return guild_name

# Formatting Rank API Value to Something Usually Used
def formatRank(trank):
	if trank == 'MVP_PLUS':
		return 'MVP+'
	if trank == 'MVP':
		return 'MVP'
	if trank == 'VIP_PLUS':
		return 'VIP+'
	if trank == 'VIP':
		return 'VIP'
	else:
		return 'Non'

# 'Main' Function
def stalkPerson(username):
	player_uuid = getUUID(username)

	if player_uuid == 'no':
		return ['no']

	p_status = check_status(player_uuid)
	p_status = format_status(player_uuid)

	p_guild = get_guild(player_uuid)

	playerdata_hypixel = get("https://api.hypixel.net/player?key=%s&uuid=%s" % (api_key, player_uuid)).json()

	username = playerdata_hypixel['player']['displayname']

	p_karma = playerdata_hypixel['player']['karma']

	p_rank = playerdata_hypixel['player']['newPackageRank']
	p_rank = formatRank(p_rank)

	details = [username, p_rank, p_status, p_guild, p_karma]
	
	return details


# playerdata_hypixel = get("https://api.hypixel.net/player?key=%s&uuid=%s" % (api_key, uuid)).json()
# playerdata_guild = get("https://api.hypixel.net/guild?key=%s&player=%s" % (api_key, uuid)).json()
# playerdata_status = get("https://api.hypixel.net/status?key=%s&uuid=%s" % (api_key, uuid)).json()