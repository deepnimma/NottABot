import logging
import os
from dotenv import load_dotenv
from requests import get
import random
import time
import discord
from discord.ext import commands

try:
    import cogs.convertLogging as cl
except:
    import convertLogging as cl

load_dotenv()
log_level = os.getenv("LOGLEVEL")
api_key = os.getenv("APIKEY")
discord_log_level = os.getenv("DISCORD_LOG_LEVEL")

log = logging.getLogger(__name__)
log = cl.getLogging(log_level, discord_log_level)

def getUUID(username):
    log.debug(f"getUUID called for {username}")
    try:
        log.debug("Requesting Mojang Data")
        data = get(f"https://api.mojang.com/users/profiles/minecraft/{username}").json()
        log.debug("Mojang Data Received, Returning UUID")

        return data["id"]
    except:
        log.error("Username not Found, Returning")
        return "no"


def getProfileCuteNames(uuid):
    profs = []
    playerdata = get(
        "https://api.hypixel.net/player?key=%s&uuid=%s" % (api_key, uuid)
    ).json()
    for i in playerdata["player"]["stats"]["SkyBlock"]["profiles"]:
        profs.append(i)

    return profs


def getProfiles(uuid):
    profs = []
    playerdata = get(
        "https://api.hypixel.net/player?key=%s&uuid=%s" % (api_key, uuid)
    ).json()
    for i in playerdata["player"]["stats"]["SkyBlock"]["profiles"]:
        profs.append(
            playerdata["player"]["stats"]["SkyBlock"]["profiles"][i]["cute_name"]
        )

    return profs


def checkUsername(username: str):
    log.debug(f"Checking {username}")
    data = get(f"https://sky.shiiyu.moe/api/v2/profile/{username}").json()
    log.debug(f"Data Received")

    try:
        if data["error"] == "Failed resolving username.":
            log.error("Username not Found")
            return False
    except:
        log.debug("Username Found")
        return True


def getLatestProfile(uuid):
    # uuid = getUUID(username)

    playerdata = get(
        "https://api.hypixel.net/player?key=%s&uuid=%s" % (api_key, uuid)
    ).json()

    j = 1
    latest_profile = []

    for i in playerdata["player"]["stats"]["SkyBlock"]["profiles"]:
        if j == 1:
            latest_profile = playerdata["player"]["stats"]["SkyBlock"]["profiles"][i][
                "cute_name"
            ]
            latest_profile_id = playerdata["player"]["stats"]["SkyBlock"]["profiles"][
                i
            ]["profile_id"]
            j += 1

    return latest_profile, latest_profile_id


def convertTeammates(teammates):
    log.info(f"Converting {teammates}")
    teammatesConverted = []
    for teammate in teammates:
        log.debug(f"Converting {teammate}")

        log.debug(f"Requesting From MojangAPI")
        names = get(f"https://api.mojang.com/user/profiles/{teammate}/names").json()
        log.debug(f"Received Name Data")

        realName = ""

        for name in names:
            realName = name["name"]
        # name = name['name']

        log.debug(f"Name Found : {realName}")
        teammatesConverted.append(name["name"])

    return teammatesConverted


def getRandomColor():
    log.debug(f"getRandomColor called")
    colors = (
        0x000000,
        0xFFFFFF,
        0x028C6A,
        0xFAA2B0,
        0x82B741,
        0x00AEEF,
        0xFF9FF6,
        0x6289FF,
        0x41FF00,
        0x00FFFF,
        0x800080,
        0xFFFF00,
        0xFF0000,
        0xFF00FF,
    )

    rInt = random.randint(0, len(colors) - 1)

    log.debug(f"Random Number is: {rInt} - Color Being Returned is: {colors[rInt]}")
    return colors[rInt]


def makeString(my_list: list):
    list_string = ""

    for list_item in my_list:
        log.debug(f"Adding {list_item} to String")

        list_string += list_item + " "

    return list_string


def makeString(my_list: tuple):
    list_string = ""

    for list_item in my_list:
        log.debug(f"Adding {list_item} to String\r")

        list_string += list_item + " "

    return list_string


# print(convertTeammates(["e2deec367d8c4ddb92fe8507dbdbdd33"]))


class UsernameNotFoundError(Exception):
    pass


if __name__ == "__main__":
    for i in range(0, 100):
        print(f"{getRandomColor()}")
