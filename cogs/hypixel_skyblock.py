import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
from requests import get
import logging

try:
    import cogs.commonFunctions as cf
    import cogs.convertLogging as cl
    import cogs.numberformat as num
except:
    import numberformat as num
    import commonFunctions as cf
    import convertLogging as cl

load_dotenv()
api_key = os.getenv("APIKEY")
log_level = os.getenv("LOGLEVEL")
discord_log_level = os.getenv("DISCORD_LOG_LEVEL")

log = logging.getLogger(__name__)
log = cl.getLogging(log_level, discord_log_level)


async def record_usage(self, ctx):
    log.info(
        f"{ctx.author} used {ctx.command} at {ctx.message.created_at} in {ctx.guild}"
    )
    embed = discord.Embed(
        title=f"We're Working on {ctx.command}, Please Wait...",
        color=cf.getRandomColor(),
    )

    await ctx.send(embed=embed, delete_after=2)


async def finish_usage(self, ctx):
    log.info(f"{ctx.author} finished using {ctx.command} in {ctx.guild}")


class HypixelSkyblock(
    commands.Cog, name="Hypixel Skyblock", description="Skyblock Related Functions"
):
    def __init__(self, client):
        self.client = client

    # Commands
    @commands.command(
        help="Shows Skills Data for Given Username", brief="Shows Skills Data"
    )
    @commands.before_invoke(record_usage)
    @commands.after_invoke(finish_usage)
    async def skills(self, ctx, username: str):
        log.info(f"skillStats called for {username}")

        log.debug(f"Checking Username")
        if not cf.checkUsername(username):
            log.error("Username not Found")
            raise Exception("Username Not Found")
        log.debug(f"Checked Username, Continuing")

        log.debug("Getting UUID")
        uuid = cf.getUUID(username)
        log.debug("Retrieved UUID")

        names = [
            "**Combat**",
            "**Foraging**",
            "**Farming**",
            "**Enchanting**",
            "**Alchemy**",
            "**Mining**",
            "**Fishing**",
        ]

        log.debug("Retrieving Skill Data")
        levels, expremaining, exptoup = getSkills(uuid)
        log.debug("Retrived Skill Data")

        log.debug("Retrieving Skill Average")
        skill_avg = findSkillAverage(uuid)
        log.debug("Retrieved Skill Average")

        log.debug("Creating Embed")
        embedVar = discord.Embed(
            title="Skill Details", description="", color=cf.getRandomColor()
        )  # Make this Look Better In the Future
        embedVar.add_field(name="**Skill Average**", value=str(skill_avg), inline=False)

        log.debug("Adding Fields")
        for i in range(len(levels)):
            embedVar.add_field(
                name=names[i],
                value=f"Level: {levels[i]} \nProgress Percent: {round(expremaining[i] * 100 / exptoup[i], 2)}"
                + r"%"
                + f"\n {num.human_format(expremaining[i])} / {num.human_format(exptoup[i])}",
                inline=True,
            )
            log.debug(f"Added {names[i]}")

        await ctx.send(embed=embedVar)

    @commands.command(
        aliases=["purse", "money"],
        help="Bank Data for a Given Username",
        brief="Bank Data",
    )
    @commands.before_invoke(record_usage)
    @commands.after_invoke(finish_usage)
    async def bank(self, ctx, username: str):
        if not cf.checkUsername(username):
            log.error("Username not Found")
            raise Exception("Username Not Found")

        log.debug("Getting Bank Data")
        bank, purse = getBankBalance(cf.getUUID(username))

        if bank == "no" and purse == "no":
            log.error(f"Bank API is Off for {username}")
            await ctx.send(f"Bank API is Off For This Player - {username}")
            return

        log.debug("Making Embed")
        embed = discord.Embed(title="Bank Details", color=cf.getRandomColor())
        embed.add_field(name="Bank", value=f"```{bank}```", inline=True)
        embed.add_field(name="Purse", value=f"```{purse}```", inline=True)
        log.debug("Made Embed")

        await ctx.send(embed=embed)

    @commands.command(
        help="Shows Talismans of the Given Username", brief="Shows Talismans"
    )
    @commands.before_invoke(record_usage)
    @commands.after_invoke(finish_usage)
    async def talismans(self, ctx, username):
        if not cf.checkUsername(username):
            log.error("Username not Found")
            raise Exception("Username Not Found")

        log.debug("Calling getMissingTalisman command")
        mtali = getMissingTalismans(username)
        log.debug("Retrieved Missing Talisman Command")

        log.debug("Creating Embed")
        embedVar = discord.Embed(
            title="Missing Talismans", description="", color=cf.getRandomColor()
        )
        log.debug("Created Embed")

        mtalis = ""

        for i in range(len(mtali)):
            log.debug(f"Adding {mtali[i]} to string")

            mtalis = mtalis + mtali[i] + "\n"

        embedVar.add_field(name="**Missing Talismans**", value=mtalis, inline=False)

        await ctx.send(embed=embedVar)

    @commands.command(
        help="Shows Fairy Souls of Given Username", brief="Shows Fairy Souls"
    )
    @commands.before_invoke(record_usage)
    @commands.after_invoke(finish_usage)
    async def fairysouls(self, ctx, username):
        if not cf.checkUsername(username):
            log.error("Username not Found")
            raise Exception("Username Not Found")

        log.debug(f"Calling Fairy Souls Command")
        soulsData = getFairySoulData(username)
        log.debug(f"Retrieved Fairy Souls Data")

        collectedSouls = soulsData[0]
        totalSouls = soulsData[1]

        embed = discord.Embed(title="Fairy Soul Data", color=cf.getRandomColor())
        embed.add_field(
            name="Data",
            value=f"Collected Souls: {collectedSouls}\nTotal Souls: {totalSouls}\nProgress: {round(collectedSouls * 100 / totalSouls, 2)}",
        )

        await ctx.send(embed=embed)

    @commands.command(help="Shows Pets of the Given Username", brief="Shows Pets")
    @commands.before_invoke(record_usage)
    @commands.after_invoke(finish_usage)
    async def pets(self, ctx, username):
        if not cf.checkUsername(username):
            log.error("Username not Found")
            raise Exception("Username Not Found")

        log.debug(f"Requesting Pets Data")
        petstuff = getPets(username)
        log.debug(f"Requested Pets Data")

        log.debug(f"Creating Embed")
        embed = discord.Embed(title=f"Pets of {username}", color=cf.getRandomColor())
        log.debug(f"Created Embed")

        outstring = ""

        for pet in petstuff:
            log.debug(f"Adding {pet} to outstring")
            outstring += pet + "\n"

        embed.add_field(
            name="**Pets**", value="```\n" + outstring + "```", inline=False
        )

        await ctx.send(embed=embed)

    @commands.command(
        help="Shows Missing Pets of a Given Username", brief="Shows Missing Pets"
    )
    @commands.before_invoke(record_usage)
    @commands.after_invoke(finish_usage)
    async def misspets(self, ctx, username):
        if not cf.checkUsername(username):
            log.error("Username not Found")
            raise Exception("Username Not Found")

        log.debug(f"Requesting Pets Data")
        petstuff = getMissingPets(username)
        log.debug(f"Requested Pets Data")

        log.debug(f"Creating Embed")
        embed = discord.Embed(title=f"Pets of {username}", color=cf.getRandomColor())
        log.debug(f"Created Embed")

        outstring = ""

        for pet in petstuff:
            log.debug(f"Adding {pet} to outstring")
            outstring += pet + "\n"

        embed.add_field(
            name="**Missing Pets**", value="```\n" + outstring + "```", inline=False
        )

        await ctx.send(embed=embed)

    @commands.command(
        help="Shows Top 10 Kills of the Username", brief="Top 10 Kill Count Mobs"
    )
    @commands.before_invoke(record_usage)
    @commands.after_invoke(finish_usage)
    async def topkills(self, ctx, username):
        if not cf.checkUsername(username):
            log.error("Username not Found")
            raise Exception("Username Not Found")

        log.debug(f"Requesting Kill Data")
        names, count, totalKills = get10Kills(username)
        log.debug(f"Requested Kill Data")

        log.debug(f"Creating Embed")
        embed = discord.Embed(title=f"Kills of {username}", color=cf.getRandomColor())
        log.debug(f"Created Embed")

        outstring = ""

        for i in range(len(names)):
            log.debug(f"adding {names[i]} to string")
            outstring = outstring + f"{i + 1}. {names[i]} : {count[i]} \n"

        embed.add_field(
            name="**Top 10 Kills**",
            value="```python\n" + outstring + "```",
            inline=False,
        )
        embed.add_field(
            name="**Total Number of Kills**",
            value="```python\n" + num.comma(totalKills) + "```",
            inline=False,
        )

        await ctx.send(embed=embed)

    @commands.command(help="All Kills of a Username")
    @commands.before_invoke(record_usage)
    @commands.after_invoke(finish_usage)
    async def allkills(self, ctx, username):
        if not cf.checkUsername(username):
            log.error("Username not Found")
            raise Exception("Username Not Found")

        log.debug(f"Requesting Kill Data")
        names, count, totalKills = allKills(username)
        log.debug(f"Requested Kill Data")

        log.debug(f"Creating Embed")
        embed = discord.Embed(title=f"Kills of {username}", color=cf.getRandomColor())
        log.debug(f"Created Embed")

        outstring = ""

        for i in range(len(names)):
            log.debug(f"adding {names[i]} to string")
            outstring = outstring + f"{i + 1}. {names[i]} : {count[i]} \n"

            if len(outstring) >= 1950:
                log.error("outstring length >= 1950, quitting loop to send message")
                break

        await ctx.send("```" + outstring + "```")

    # Errors
    @skills.error
    async def skills_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please Send a Username Along With the Command")
        if isinstance(error, Exception):
            await ctx.send("Username Not Found")

    @bank.error
    async def bank_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please Send a Username Along With the Command")
        if isinstance(error, Exception):
            await ctx.send("Username Not Found")

    @talismans.error
    async def talismans_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please Send a Username Along With the Command")
        if isinstance(error, Exception):
            await ctx.send(Exception.message)

    @pets.error
    async def pets_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please Send a Username Along With the Command")
        if isinstance(error, Exception):
            await ctx.send("Username Not Found")

    @misspets.error
    async def misspets_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please Send a Username Along With the Command")
        if isinstance(error, Exception):
            await ctx.send("Username Not Found")

    @topkills.error
    async def topkills_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please Send a Username Along With the Command")
        if isinstance(error, Exception):
            await ctx.send("Username Not Found")

    # @allkills.error
    # async def allkills_error(self, ctx, error):
    #     if isinstance(error, commands.MissingRequiredArgument):
    #         await ctx.send('Please Send a Username Along With the Command')
    #     if isinstance(error, Exception):
    #         await ctx.send('Username Not Found')


def setup(client):
    client.add_cog(HypixelSkyblock(client))


def getFairySoulData(username):
    log.info(f"getFairySoulData Called for {username}")

    log.debug("Retrieving Profile Data")
    latest_profile, latest_profile_id = cf.getLatestProfile(cf.getUUID(username))
    log.debug("Retrieved Profile Data")

    log.debug(f"Retrieving Data")
    data = get(f"https://sky.shiiyu.moe/api/v2/profile/{username}").json()["profiles"][
        latest_profile_id
    ]["data"]["fairy_souls"]
    log.debug(f"Retrieved Data")

    collectedSouls = data["collected"]
    totalSouls = data["total"]

    log.debug("Returning and Exiting from getFairySoulData")
    return [collectedSouls, totalSouls]


def getBankBalance(uuid):
    log.info("getBankBalance Called")

    log.debug("Getting Profile Data")
    profile_name, profile_id = cf.getLatestProfile(uuid)
    log.debug("Received Profile Data")

    log.debug("Getting SBData")
    sbdata = get(
        "https://api.hypixel.net/skyblock/profile?key=%s&profile=%s"
        % (api_key, profile_id)
    ).json()
    log.debug("Got Debug Data")

    try:
        log.debug("Got Bank Details")
        bank_money = sbdata["profile"]["banking"]["balance"]
        purse = sbdata["profile"]["members"][uuid]["coin_purse"]
    except:
        log.error("Bank API is Off")
        return "no", "no"

    log.debug("Returning, Exiting")
    return num.comma(round(bank_money, 2)), num.comma(round(purse, 2))


def formatExp(exp):
    log.debug(f"formatExp called with exp: {exp}")
    exptoup = [
        0,
        50,
        125,
        200,
        300,
        500,
        750,
        1000,
        1500,
        2000,
        3500,
        5000,
        7500,
        10000,
        15000,
        20000,
        30000,
        50000,
        75000,
        100000,
        200000,
        300000,
        400000,
        500000,
        600000,
        700000,
        800000,
        900000,
        1000000,
        1100000,
        1200000,
        1300000,
        1400000,
        1500000,
        1600000,
        1700000,
        1800000,
        1900000,
        2000000,
        2100000,
        2200000,
        2300000,
        2400000,
        2500000,
        2600000,
        2750000,
        2900000,
        3100000,
        3400000,
        3700000,
        4000000,
        4300000,
        4600000,
        4900000,
        5200000,
        5500000,
        5800000,
        6100000,
        6400000,
        6700000,
        7000000,
    ]

    i = 0

    while exp >= exptoup[i] and i in range(len(exptoup) - 1):
        exp -= exptoup[i]
        i += 1

    log.debug("Calculated Exp Requirements, Returning")
    return (i if i == 60 else i - 1), exp, exptoup[i]


def getSkills(uuid):
    log.info(f"getSkills called for {uuid}")

    log.debug(f"Retrieving Profile Data")

    profile_name, profile_id = cf.getLatestProfile(uuid)
    log.debug(f"Retrieved Profile Data")
    log.debug(f"Retrieving SBData")

    sbdata = get(
        "https://api.hypixel.net/skyblock/profile?key=%s&profile=%s"
        % (api_key, profile_id)
    ).json()

    log.debug(f"Retrieved SBData")

    datap = sbdata["profile"]["members"][uuid]

    log.debug(f"Assigning Values")
    combat, combatexp, combattoup = formatExp(
        round(datap["experience_skill_combat"], 2)
    )
    foraging, foragingexp, foragingtoup = formatExp(
        round(datap["experience_skill_foraging"], 2)
    )
    farming, farmingexp, farmingtoup = formatExp(
        round(datap["experience_skill_farming"], 2)
    )
    enchanting, enchantingexp, enchantingtoup = formatExp(
        round(datap["experience_skill_enchanting"], 2)
    )
    alchemy, alchemyexp, alchemytoup = formatExp(
        round(datap["experience_skill_alchemy"], 2)
    )
    mining, miningexp, miningtoup = formatExp(
        round(datap["experience_skill_mining"], 2)
    )
    fishing, fishingexp, fishingtoup = formatExp(
        round(datap["experience_skill_fishing"], 2)
    )
    log.debug(f"Assigned Values, Returning")
    log.info("Returning from getSkills")
    return (
        [combat, foraging, farming, enchanting, alchemy, mining, fishing],
        [
            combatexp,
            foragingexp,
            farmingexp,
            enchantingexp,
            alchemyexp,
            miningexp,
            fishingexp,
        ],
        [
            combattoup,
            foragingtoup,
            farmingtoup,
            enchantingtoup,
            alchemytoup,
            miningtoup,
            fishingtoup,
        ],
    )


def findSkillAverage(uuid):
    log.debug("Getting Skill Average")
    p, c, d = getSkills(uuid)

    sum = 0

    for i in p:
        log.debug(f"Adding {i} to {p}")
        sum += i

    log.debug("Found Skill Average, Returning")
    return round(sum / 7, 2)


def getMissingTalismans(username):
    log.info(f"getMissingTalismans called for {username}")
    missing_talismans = []

    log.debug("Getting Profile Data")

    latest_profile, latest_profile_id = cf.getLatestProfile(cf.getUUID(username))

    log.debug("Retrieved Profile Data")
    log.debug("Retrieving SB Data")

    data = get(f"https://sky.shiiyu.moe/api/v2/profile/{username}").json()
    data = data["profiles"][latest_profile_id]["data"]["missingTalismans"]["missing"]

    log.debug("Retrieved Data")
    # print(data)
    # missing_talismans = ['test_talisman']

    for i in range(len(data)):
        tali = data[i]["display_name"]

        log.debug(f"Appending {tali}")

        if tali == "Beastmaster Crest":
            log.warning(f"Beastmaster Crest Found")

            tali = tali + " - " + data[i]["rarity"].capitalize()

        missing_talismans.append(tali)

    log.debug("Returning Missing Talismans")
    return missing_talismans


def getPets(username):
    log.info(f"getPets called for {username}")

    log.debug(f"Retrieving Profile Data")
    profile, profile_id = cf.getLatestProfile(cf.getUUID(username))
    log.debug(f"Retrieved Profile Data")

    log.debug(f"Retrieving Data")
    data = get("https://sky.shiiyu.moe/api/v2/profile/%s" % (username)).json()
    log.debug(f"Retrieved Data")

    data = data["profiles"][profile_id]["data"]["pets"]

    pets = []

    for i in data:
        log.debug(
            f"Appending %s - %s"
            % (
                i["rarity"].capitalize()
                + " "
                + i["display_name"].capitalize()
                + " - Level "
                + str(i["level"]["level"]),
                i["emoji"],
            )
        )
        pets.append(
            i["rarity"].capitalize()
            + " "
            + i["display_name"].capitalize()
            + " - Level "
            + str(i["level"]["level"])
            + " "
            + i["emoji"]
        )

    log.info("Returning From Pets Function")
    return pets


def getMissingPets(username):
    log.info(f"getMissingPets called for {username}")

    log.debug(f"Requesting Latest Profile Data")
    profile, profile_id = cf.getLatestProfile(cf.getUUID(username))
    log.debug(f"Requested Latest Profile Data")

    log.debug(f"Requesting Data")
    data = get("https://sky.shiiyu.moe/api/v2/profile/%s" % (username)).json()
    log.debug(f"Requested Data")

    data = data["profiles"][profile_id]["data"]["missingPets"]

    pets = []

    for i in data:
        log.debug(f"Appending %s - %s" % (i["display_name"].capitalize(), i["emoji"]))
        pets.append(i["display_name"].capitalize() + " " + i["emoji"])

    log.info("Returning from getMissingPets function")
    return pets


def get10Kills(username):
    log.info(f"get10Kills called for {username}")

    log.debug(f"Retrieving Profile Data")
    _, profile_id = cf.getLatestProfile(cf.getUUID(username))
    log.debug(f"Retrieved Profile Data")

    log.debug(f"Requesting Data")
    data = get("https://sky.shiiyu.moe/api/v2/profile/%s" % (username)).json()
    log.debug(f"Retrieved Data")

    data = data["profiles"][profile_id]["data"]["kills"]

    names = []
    lencount = []
    i = 0

    totalCount = 0

    for i in range(len(data)):
        if i >= 10:
            log.debug(f"Index Greater Than 10, Breaking")
            break

        names.append(data[i]["entityName"])
        lencount.append(num.comma(data[i]["amount"]))

        log.debug(
            f'{i + 1}. Appending {data[i]["entityName"]} with count: {num.comma(data[i]["amount"])}'
        )

    for i in range(len(data)):
        log.debug(f'Adding {data[i]["amount"]} to {totalCount}')

        totalCount += data[i]["amount"]

    return names, lencount, totalCount


def allKills(username):
    log.info(f"allkills called for {username}")

    log.debug(f"Retrieving Profile Data")
    _, profile_id = cf.getLatestProfile(cf.getUUID(username))
    log.debug(f"Retrieved Profile Data")

    log.debug(f"Requesting Data")
    data = get("https://sky.shiiyu.moe/api/v2/profile/%s" % (username)).json()
    log.debug(f"Retrieved Data")

    data = data["profiles"][profile_id]["data"]["kills"]

    names = []
    lencount = []
    i = 0

    totalCount = 0

    for i in range(len(data)):
        if data[i]["amount"] <= 50:
            log.debug(f"Num Kills Less Than 50, Breaking")
            break

        names.append(data[i]["entityName"])
        lencount.append(num.comma(data[i]["amount"]))

        log.debug(
            f'{i + 1}. Appending {data[i]["entityName"]} with count: {num.comma(data[i]["amount"])}'
        )

    for i in range(len(data)):
        log.debug(f'Adding {data[i]["amount"]} to {totalCount}')

        totalCount += data[i]["amount"]

    return names, lencount, totalCount
