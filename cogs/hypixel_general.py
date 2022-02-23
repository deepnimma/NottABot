import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
from requests import get
import logging
import time

try:
    import cogs.commonFunctions as cf
    import cogs.numberformat as num
except:
    import commonFunctions as cf
    import numberformat as num

load_dotenv()
api_key = os.getenv("APIKEY")
log_level = os.getenv("LOGLEVEL")
discord_log_level = os.getenv("DISCORD_LOG_LEVEL")

try:
    import cogs.convertLogging as cl
except:
    import convertLogging as cl

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


class HypixelGeneral(
    commands.Cog, name="Hypixel General", description="General Hypixel Functions"
):
    def __init__(self, client):
        self.client = client

    # Commands
    @commands.command(help="Basic Details of Given Username")
    @commands.before_invoke(record_usage)
    @commands.after_invoke(finish_usage)
    async def hystalk(self, ctx, username: str):
        log.debug("Requesting UUID")
        uuid = cf.getUUID(username)
        log.debug("Received UUID")

        # if uuid == 'no':
        #     raise commands.CommandError

        log.debug("Receiving Data")
        log.debug("Requesting Details")
        details = hystalkdata(uuid)
        log.debug("Received Details")

        username = details[0]
        rank = details[1]
        status = details[2]
        guild = details[3]
        karma = details[4]

        log.debug("Creating Embed")
        embedvar = discord.Embed(
            title=f"{username}'s Player Details",
            description="",
            color=cf.getRandomColor(),
        )
        embedvar.add_field(name="Username: ", value=username, inline=False)
        embedvar.add_field(name="Rank: ", value=rank, inline=True)
        embedvar.add_field(name="Guild: ", value=guild, inline=True)
        embedvar.add_field(name="Karma: ", value=num.comma(karma), inline=True)
        embedvar.add_field(name="Current Status: ", value=status, inline=False)
        log.debug("Created Embed Sending")
        log.debug("Sending Embed")

        await ctx.send(embed=embedvar)

    # Errors
    @hystalk.error
    async def hystalk_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            log.error("Missing Username")
            await ctx.send("Please Send a Username Along With the Command")
        if isinstance(error, commands.CommandError):
            log.error("Username Not Found")
            await ctx.send("Username Not Found")


def setup(client):
    client.add_cog(HypixelGeneral(client))


def hystalkdata(uuid):
    log.info(f"hystalkdata called for {uuid}")

    log.debug("Calling Status Function")
    status = formatStatus(checkStatus(uuid))
    log.debug("Received Status")
    log.debug("Calling Guild Function")
    guild = getGuild(uuid)
    log.debug("Received Guild")

    log.debug("Requesting Hypixel Data")
    hyp_data = get(f"https://api.hypixel.net/player?key={api_key}&uuid={uuid}").json()
    log.debug("Received Hypixel Data")

    log.debug("Assigning Variables")
    username = hyp_data["player"]["displayname"]
    karma = hyp_data["player"]["karma"]
    rank = formatRank(hyp_data["player"]["newPackageRank"])

    log.debug("Returning Variables")
    return [username, rank, status, guild, karma]


def checkStatus(uuid):
    log.info(f"checkStatus called for {uuid}")

    log.debug("Requesting Hypixel Data")
    data = get(f"https://api.hypixel.net/status?key={api_key}&uuid={uuid}").json()
    log.debug("Hypixel Data Received")

    log.debug("Returning Hypixel Data")
    return data["session"]["online"]


def formatStatus(status):
    if not status:
        log.debug("Player is Offline")
        return "Offline"
    else:
        log.debug("Player is Online")
        return "Online"


def getGuild(uuid):
    log.info(f"getGuild Called for {uuid}")

    log.debug(f"Requesting Hypixel Data")
    data = get(f"https://api.hypixel.net/guild?key={api_key}&player={uuid}").json()
    log.debug(f"Hypixel Data Received")

    # If Player Guild Exists Return Guild Name, Otherwise Return 'No Guild'
    if data["guild"] is None:
        log.debug("Player isn't In Any Guild, Returning")
        return "No Guild"

    log.debug("Returning Guild Name")
    return data["guild"]["name"]


def formatRank(rank):
    if rank == "MVP_PLUS":
        log.debug("Rank is MVP+")
        return "MVP+"
    elif rank == "VIP_PLUS":
        log.debug("Rank is VIP+")
        return "VIP+"
    elif rank != "VIP" and rank != "MVP":
        log.debug("Rank is None")
        return "Non"
    else:
        log.debug("Rank is Either VIP or MVP")
        return rank
