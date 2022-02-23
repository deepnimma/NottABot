# Importing Packages
import discord
from discord.ext import commands, tasks
import os
from dotenv import load_dotenv
from pathlib import Path
import json
import coloredlogs
import logging
import datetime

import cogs.convertLogging as cl

# Updating Times Ran Counter and Last Date Run Files
if not os.path.exists("./Data/BotData/timeRun.txt"):
    with open("./Data/BotData/timeRun.txt", "w") as file:
        file.write("0")
if not os.path.exists("./Data/BotData/lastDateRun.txt"):
    with open("./Data/BotData/lastDateRun.txt", "w") as file:
        file.write(str(datetime.datetime.now(datetime.timezone.utc)) + " UTC")

with open("./Data/BotData/timeRun.txt", "r+") as ran:
    st = int(ran.read())
    st += 1

with open("./Data/BotData/timeRun.txt", "w") as ran:
    ran.write(str(st))
with open("./Data/BotData/lastDateRun.txt", "w") as timeLast:
    timeLast.write(str(datetime.datetime.now(datetime.timezone.utc)) + " UTC")

# Importing Data from .env
load_dotenv()
env_path = Path(".") / ".env"
api_key = os.getenv("API")
BOTTOKEN = os.getenv("BOTTOKEN")
log_level = os.getenv("LOGLEVEL")
discord_log_level = os.getenv("DISCORD_LOG_LEVEL")

log = logging.getLogger(__name__)
log = cl.getLogging(log_level, discord_log_level)

log.info("Logging Setup")

log.critical(f"This is the {st} time this bot has been run")


def get_prefix(client, message):
    with open("prefixes.json", "r") as file:
        prefixes = json.load(file)

    return prefixes[str(message.guild.id)]


# Making the Client
client = commands.Bot(command_prefix=get_prefix)


async def record_usage(ctx):
    print(ctx.author, "used", ctx.command, "at", ctx.message.created_at)


# def updateBazaar():
#
#
#
# @tasks.loop(minutes=30)
# async def updateBazaarData():


# Events
@client.event
async def on_guild_join(guild):
    log.critical("Joined {}".format(guild.id))
    with open("prefixes.json", "r") as file:
        log.debug("Loading Prefixes File")
        prefixes = json.load(file)

    log.info("Setting Guild Prefix")
    prefixes[str(guild.id)] = "*"

    with open("prefixes.json", "w") as file:
        log.debug("Dumping Prefix Into Json File")
        json.dump(prefixes, file, indent=4)


@client.event
async def on_guild_remove(guild):
    log.critical("Removed from {}".format(guild.id))
    with open("prefixes.json", "r") as file:
        log.debug("Loading Prefixes File")
        prefixes = json.load(file)

    log.info("Removing Guild Prefix")
    prefixes.pop(str(guild.id))

    with open("prefixes.json", "w") as file:
        log.debug("Dumping Prefix Into Json File")
        json.dump(prefixes, file, indent=4)


# Commands
@client.command(hidden=True)
@commands.before_invoke(record_usage)
async def load(ctx, extension):
    if ctx.author.id != 250257390643970059:
        return

    try:
        log.debug(f"Sending Message to ctx")
        await ctx.send(f"Loading {extension}")
    except:
        log.error(f"Couldn't Send Message to ctx")

    log.info(f"Loading {extension}")
    client.load_extension(f"cogs.{extension}")
    log.info(f"Loaded {extension}")

    try:
        await ctx.send(f"Loaded {extension}")
        log.info(f"Sending Message to ctx")
    except:
        log.error(f"Couldn't Send Message to ctx")


@client.command(hidden=True)
@commands.before_invoke(record_usage)
async def unload(ctx, extension):
    if ctx.author.id != 250257390643970059:
        return

    try:
        log.debug(f"Sending Message to ctx")
        await ctx.send(f"Loading {extension}")
    except:
        log.error(f"Couldn't Send Message to ctx")

    log.info(f"Loading {extension}")
    client.unload_extension(f"cogs.{extension}")
    log.info(f"Loaded {extension}")

    try:
        await ctx.send(f"Loaded {extension}")
        log.info(f"Sending Message to ctx")
    except:
        log.error(f"Couldn't Send Message to ctx")


@client.command(hidden=True)
@commands.before_invoke(record_usage)
async def reloadcogs(ctx):
    if ctx.author.id != 250257390643970059:
        return

    if str(ctx.author) != "NottCurious#4351":
        log.error(f"{ctx.author} isn't NottCurious")
        await ctx.send("You Are Not Allowed to Use This Command")
        return

    await ctx.send("Reloading Cogs")
    log.info("Reloading Cogs")
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            if filename == "numberformat.py":
                log.debug("Skipping numberformat.py")
                continue

            if filename == "commonHypixelFunctions.py":
                log.debug("Skipping commonHypixelFunctions.py")
                continue

            try:
                client.load_extension(f"cogs.{filename[:-3]}")
                log.info(f"Loading {filename}")
            except:
                log.error(f"Couldn't Load {filename}")
                continue
            # client.load_extension(f'cogs.{filename[:-3]}')

    await ctx.send("Cogs Reloaded", delete_after=2)
    log.info("Reloaded Cogs")


@client.command(hidden=True)
@commands.before_invoke(record_usage)
async def listCogs(ctx):
    if ctx.author.id != 250257390643970059:
        return

    filenames = ""
    embedvar = discord.Embed(title="List of Cogs", description="", colour=0x00FF00)
    log.debug("Creating String for Embed")
    for file in os.listdir("./cogs"):
        if file.endswith(".py"):
            if filename == "numberformat.py":
                log.debug("Skipping numberformat.py")
                continue

            if filename == "commonHypixelFunctions.py":
                log.debug("Skipping commonHypixelFunctions.py")
                continue
            # embedvar.add_field(name=file, value='', inline=False)
            # await ctx.send(file)
            log.debug(f"Adding {file} to String")
            filenames += file + "\n"

    log.debug("Created Embed")
    embedvar.add_field(name="Cogs:", value=filenames, inline=True)
    log.debug("Created Embed")

    await ctx.send(embed=embedvar)
    log.info("Sent Embed of Cogs")


log.info("Loading Cogs")
for filename in os.listdir("./cogs"):
    skip_files = ("numberformat.py", "commonFunctions.py", "convertLogging.py")

    if filename.endswith(".py"):
        if filename in skip_files:
            log.warning(f"Skipping {filename}")
            continue

        log.debug(f"Loading {filename}")
        client.load_extension(f"cogs.{filename[:-3]}")
log.info("Loaded Cogs")


# Letting the Client Run
client.run(BOTTOKEN)
