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
    import commonFunctions as cf
    import convertLogging as cl
    import numberformat as num

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


class Slayers(commands.Cog, description="Slayer Related Functions"):
    def __init__(self, client):
        self.client = client

    @commands.command(help="Shows 3 Slayer Monsters Data")
    @commands.before_invoke(record_usage)
    @commands.after_invoke(finish_usage)
    async def slayers(self, ctx, username: str):
        if not cf.checkUsername(username):
            log.error(f"{username} doesn't Exist")
            raise Exception("Username Not Found")

        log.debug(f"Requesting Data from All 3 Functions")
        revenant_data = getSlayerData(username, "zombie")
        tarantula_data = getSlayerData(username, "spider")
        sven_data = getSlayerData(username, "wolf")
        log.debug(f"Finished Requesting Data from all 3 Functions")

        log.debug(f"Creating Embed")
        embed = discord.Embed(title="Slayer Data", color=cf.getRandomColor())
        log.debug(f"Created Embed")

        log.debug(f"Adding Fields")
        log.debug(f"Adding Current Data")

        embed.add_field(name="Revenant", value=revenant_data[0], inline=True)
        embed.add_field(name="Tarantula", value=tarantula_data[0], inline=True)
        embed.add_field(name="Sven", value=sven_data[0], inline=True)

        log.debug(f"Added Current Data")
        log.debug(f"Adding Kills")

        embed.add_field(name="Revenant", value=revenant_data[3], inline=True)
        embed.add_field(name="Tarantula", value=tarantula_data[3], inline=True)
        embed.add_field(name="Sven", value=sven_data[3], inline=True)

        log.debug(f"Added Kills")
        log.debug(f"Adding To Next")

        embed.add_field(name="Revenant", value=revenant_data[1], inline=True)
        embed.add_field(name="Tarantula", value=tarantula_data[1], inline=True)
        embed.add_field(name="Sven", value=sven_data[1], inline=True)

        log.debug(f"Added To Next")
        log.debug(f"Adding To Next w/ Aatrox")

        embed.add_field(name="Revenant", value=revenant_data[2], inline=True)
        embed.add_field(name="Tarantula", value=tarantula_data[2], inline=True)
        embed.add_field(name="Sven", value=sven_data[2], inline=True)

        log.debug(f"Added To Next w/ Aatrox")
        log.debug(f"Coins Spent")

        embed.add_field(name="Revenant", value=revenant_data[4], inline=True)
        embed.add_field(name="Tarantula", value=tarantula_data[4], inline=True)
        embed.add_field(name="Sven", value=sven_data[4], inline=True)

        log.debug(f"Added Coins Spent")
        log.debug(f"Adding Total Coins Spent")

        embed.add_field(
            name="Total Coins Spent",
            value=f"```{num.comma(revenant_data[5] + tarantula_data[5] + sven_data[5])}```",
            inline=False,
        )

        log.debug(f"Created Embed")

        await ctx.send(embed=embed)

    # Commands
    @commands.command(help="Shows Revenant Data for Given Username")
    @commands.before_invoke(record_usage)
    @commands.after_invoke(finish_usage)
    async def revenant(self, ctx, username: str):
        if not cf.checkUsername(username):
            log.error(f"{username} doesn't Exist")
            raise Exception("Username Not Found")

        log.debug(f"Calling Data Command")
        data = getSlayerData(username, "zombie")
        log.debug(f"Called Data Command")

        log.debug(f"Created Embed")
        embed = discord.Embed(title="Zombie Slayer", color=cf.getRandomColor())
        embed.add_field(name="Current Data", value=data[0], inline=False)
        embed.add_field(name="Kills", value=data[3], inline=False)
        embed.add_field(name="To Next", value=data[1], inline=False)
        embed.add_field(name="To Next (w/ Aatrox)", value=data[2], inline=False)
        embed.add_field(name="Coins Spent", value=data[4], inline=False)
        log.debug("Embed Created")

        log.debug(f"Sent Embed")
        await ctx.send(embed=embed)

    @commands.command(help="Shows Tarantula Data for Given Username")
    @commands.before_invoke(record_usage)
    @commands.after_invoke(finish_usage)
    async def tarantula(self, ctx, username: str):
        if not cf.checkUsername(username):
            log.error(f"{username} doesn't Exist")
            raise Exception("Username Not Found")

        log.debug(f"Calling Data Command")
        data = getSlayerData(username, "spider")
        log.debug(f"Called Data Command")

        log.debug(f"Created Embed")
        embed = discord.Embed(title="Spider Slayer", color=cf.getRandomColor())
        embed.add_field(name="Current Data", value=data[0], inline=False)
        embed.add_field(name="Kills", value=data[3], inline=False)
        embed.add_field(name="To Next", value=data[1], inline=False)
        embed.add_field(name="To Next (w/ Aatrox)", value=data[2], inline=False)
        embed.add_field(name="Coins Spent", value=data[4], inline=False)
        log.debug("Embed Created")

        log.debug(f"Sent Embed")
        await ctx.send(embed=embed)

    @commands.command(help="Shows Sven Data for Given Username")
    @commands.before_invoke(record_usage)
    @commands.after_invoke(finish_usage)
    async def sven(self, ctx, username: str):
        if not cf.checkUsername(username):
            log.error(f"{username} doesn't Exist")
            raise Exception("Username Not Found")

        log.debug(f"Calling Data Command")
        data = getSlayerData(username, "wolf")
        log.debug(f"Called Data Command")

        log.debug(f"Created Embed")
        embed = discord.Embed(title="Wolf Slayer", color=cf.getRandomColor())
        embed.add_field(name="Current Data", value=data[0], inline=False)
        embed.add_field(name="Kills", value=data[3], inline=False)
        embed.add_field(name="To Next", value=data[1], inline=False)
        embed.add_field(name="To Next (w/ Aatrox)", value=data[2], inline=False)
        embed.add_field(name="Coins Spent", value=data[4], inline=False)
        log.debug("Embed Created")

        log.debug(f"Sent Embed")
        await ctx.send(embed=embed)

    # Errors
    @revenant.error
    async def revenant_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please Send a Username Along With the Command")
        if isinstance(error, Exception):
            await ctx.send("Username Not Found")

    @tarantula.error
    async def tarantula_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please Send a Username Along With the Command")
        if isinstance(error, Exception):
            await ctx.send("Username Not Found")

    @sven.error
    async def sven_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please Send a Username Along With the Command")
        if isinstance(error, Exception):
            await ctx.send("Username Not Found")

    @slayers.error
    async def slayers_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please Send a Username Along With the Command")
        if isinstance(error, Exception):
            await ctx.send("Username Not Found")


def setup(client):
    client.add_cog(Slayers(client))


# Zombie Wolf and Spider
def getSlayerData(username, enemy):
    if enemy == "zombie":
        return specialRevenantFunctionBecauseZombiesAreCoolAndTheyHaveAnExtraTier(
            username
        )

    log.info(f"getSlayerData called for {username} and enemy: {enemy}")

    log.debug("Retrieving Latest Profile Data")
    _, profile_id = cf.getLatestProfile(cf.getUUID(username))
    log.debug(f"Latest Profile is {profile_id} for {username}")

    log.debug(f"Retrieving Data")
    data = get(f"https://sky.shiiyu.moe/api/v2/profile/{username}/").json()["profiles"][
        profile_id
    ]["data"]
    log.debug(f"Retrieved Data")

    log.debug(f"Assigning Data to Variables")
    coins_spent = data["slayer_coins_spent"][enemy]

    currentLevel = data["slayers"][enemy]["level"]["currentLevel"]
    xp = data["slayers"][enemy]["level"]["xp"]
    xpfornext = data["slayers"][enemy]["level"]["xpForNext"] - xp
    xpformax = 1000000 - xpfornext

    t1k = data["slayers"][enemy]["kills"]["1"]
    t2k = data["slayers"][enemy]["kills"]["2"]
    t3k = data["slayers"][enemy]["kills"]["3"]
    t4k = data["slayers"][enemy]["kills"]["4"]

    T4Next = round(xpfornext / 500, 2)
    T4Max = round(xpformax / 500, 2)
    costForNextT4 = round(xpfornext / 500, 2) * 50000
    costForMaxT4 = round(xpformax / 500, 2) * 50000
    log.debug(f"Finished Assigning Variables")

    log.debug(f"Creating Strings")
    coinsSpentStr = f"```python\n{num.comma(coins_spent)}```"
    killsStr = f"```python\nT1s Killed: {t1k}\nT2s Killed: {t2k}\nT3s Killed: {t3k}\nT4s Killed: {t4k}```"
    toNext = f"```python\nT4s For Next: {num.comma(T4Next)}\nCost For Next: {num.comma(costForNextT4)}\n\nT4s For Max: {num.comma(T4Max)}\nCost For Max: {num.comma(costForMaxT4)}```"
    toNextAatrox = f"```python\nT4s For Next: {num.comma(round(T4Next * 0.75, 2))}\nCost For Next: {num.comma(round(costForNextT4 / 2, 2))}\n\nT4s For Max: {num.comma(round(T4Max * 0.75, 2))}\nCost For Max: {num.comma(round(costForMaxT4 / 2, 2))}```"
    currentData = f"```python\nCurrent Level: {currentLevel}\nCurrent Exp: {xp}\nExp For Next: {num.comma(xpfornext)}\n```"
    log.debug(f"Created Strings")

    log.debug(f"Returning Strings")
    return [currentData, toNext, toNextAatrox, killsStr, coinsSpentStr, coins_spent]


def specialRevenantFunctionBecauseZombiesAreCoolAndTheyHaveAnExtraTier(username):
    log.info(f"getSlayerData called for {username} and enemy: zombie")

    log.debug("Retrieving Latest Profile Data")
    _, profile_id = cf.getLatestProfile(cf.getUUID(username))
    log.debug(f"Latest Profile is {profile_id} for {username}")

    log.debug(f"Retrieving Data")
    data = get(f"https://sky.shiiyu.moe/api/v2/profile/{username}/").json()["profiles"][
        profile_id
    ]["data"]
    log.debug(f"Retrieved Data")

    log.debug(f"Assigning Varibles")
    coins_spent = data["slayer_coins_spent"]["zombie"]

    currentLevel = data["slayers"]["zombie"]["level"]["currentLevel"]
    xp = data["slayers"]["zombie"]["level"]["xp"]
    xpfornext = data["slayers"]["zombie"]["level"]["xpForNext"] - xp
    xpformax = 1000000 - xpfornext

    t1k = data["slayers"]["zombie"]["kills"]["1"]
    t2k = data["slayers"]["zombie"]["kills"]["2"]
    t3k = data["slayers"]["zombie"]["kills"]["3"]
    t4k = data["slayers"]["zombie"]["kills"]["4"]

    T4Next = round(xpfornext / 500, 2)
    T5Next = round(xpfornext / 1500, 2)
    T4Max = round(xpformax / 500, 2)
    T5Max = round(xpformax / 1500, 2)
    costForNextT4 = round(xpfornext / 500, 2) * 50000
    costForNextT5 = round(xpfornext / 1500, 2) * 100000
    costForMaxT4 = round(xpformax / 500, 2) * 50000
    costForMaxT5 = round(xpformax / 1500, 2) * 100000
    log.debug(f"Assigned Variables")

    log.debug(f"Creating Strings")
    coinsSpentStr = f"```python\n{num.comma(coins_spent)}```"
    killsStr = f"```python\nT1s Killed: {t1k}\nT2s Killed: {t2k}\nT3s Killed: {t3k}\nT4s Killed: {t4k}```"
    toNext = (
        f"```python\nT4s For Next: {num.comma(T4Next)}\nCost For Next: {num.comma(costForNextT4)}\n\nT4s For Max: "
        f"{num.comma(T4Max)}\nCost For Max: {num.comma(costForMaxT4)}\n\n\n\nT5s For Next: {num.comma(T5Next)}\nCost For Next: {num.comma(costForNextT5)}\n\nT4s For Max: "
        f"{num.comma(T5Max)}\nCost For Max: {num.comma(costForMaxT5)}```"
    )
    toNextAatrox = (
        f"```python\nT4s For Next: {num.comma(round(T4Next * 0.75, 2))}\n"
        f"Cost For Next: {num.comma(round(costForNextT4 / 2, 2))}\n\nT4s For Max: "
        f"{num.comma(round(T4Max * 0.75, 2))}\nCost For Max: {num.comma(round(costForMaxT4 / 2, 2))}\n\n\n"
        f"T5s For Next: {num.comma(round(T5Next * 0.75, 2))}\n"
        f"Cost For Next: {num.comma(round(costForNextT5 / 2, 2))}\n\nT4s For Max: "
        f"{num.comma(round(T5Max * 0.75, 2))}\nCost For Max: {num.comma(round(costForMaxT5 / 2, 2))}```"
    )
    currentData = f"```python\nCurrent Level: {currentLevel}\nCurrent Exp: {xp}\nExp For Next: {num.comma(xpfornext)}\n```"
    log.debug(f"Created Strings")

    log.debug(f"Returning Strings")
    return [currentData, toNext, toNextAatrox, killsStr, coinsSpentStr, coins_spent]


def getExpToUp(level):
    if level == 0:
        log.debug(f"level is {level}")
        return 5
    elif level == 1:
        log.debug(f"level is {level}")
        return 15
    elif level == 2:
        log.debug(f"level is {level}")
        return 200
    elif level == 3:
        log.debug(f"level is {level}")
        return 1000
    elif level == 4:
        log.debug(f"level is {level}")
        return 5000
    elif level == 5:
        log.debug(f"level is {level}")
        return 20000
    elif level == 6:
        log.debug(f"level is {level}")
        return 100000
    elif level == 7:
        log.debug(f"level is {level}")
        return 400000
    elif level == 8:
        log.debug(f"level is {level}")
        return 1000000
    else:
        log.debug(f"level is {level}")
        return 1
