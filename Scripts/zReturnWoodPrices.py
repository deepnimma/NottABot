# Importing Libraries
from requests import get
from dotenv import load_dotenv
from pathlib import Path
import os

# Getting Api Key From .env File
load_dotenv()
env_path = Path('.') / '.env'
api_key = os.getenv("API_KEY")

data = get("https://api.hypixel.net/skyblock/bazaar?key=%s" % (api_key)).json()

def get_wood_prices():
	# Just Some Things To Make My Life Easier
	wood = ["ENCHANTED_OAK_LOG", "ENCHANTED_BIRCH_LOG", "ENCHANTED_SPRUCE_LOG", "ENCHANTED_JUNGLE_LOG", "ENCHANTED_DARK_OAK_LOG", "ENCHANTED_ACACIA_LOG"]
	wood_prices = []

	# Getting Prices and Putting Them Inside Wood_Prices List
	for i in wood:
	    wood_prices.append(data["products"][i]["buy_summary"][0]["pricePerUnit"])

	# Just Some Verbose

	# Giving the Values To Variables
	oak_price = str(wood_prices[0])
	birch_price = str(wood_prices[1])
	spruce_price = str(wood_prices[2])
	jungle_price = str(wood_prices[3])
	dark_oak_price = str(wood_prices[4])
	acacia_price = str(wood_prices[5])


	# Returning Values
	return [oak_price, birch_price, spruce_price, jungle_price, dark_oak_price, acacia_price]