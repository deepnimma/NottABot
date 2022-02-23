import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
from requests import get
import logging


try:
    import cogs.numberformat as num
    import cogs.commonFunctions as cf
    import cogs.convertLogging as cl
except:
    # print("le no")
    import convertLogging as cl
    import numberformat as num
    import commonFunctions as cf

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


class Dungeon(commands.Cog, description="Dungeons Related Functions"):
    def __init__(self, client):
        self.client = client

    @commands.command(
        help="Show the Details for Given Username and Floor",
        brief="Details for Given Floor",
    )
    @commands.before_invoke(record_usage)
    @commands.after_invoke(finish_usage)
    async def floor(self, ctx, username: str, floor: int = 0):

        log.debug(f"Calling Function")
        try:
            data_tuple = floorData(username=username, floor=floor)
        except:
            log.critical(f"Username not Found, Raising Exception")
            raise Exception("Username not Found")

            return

        log.debug(f"Called Function, Received Data")

        log.debug(f"Creating Embed")
        embed = discord.Embed(
            title=f"Floor Data for Username: {username} and Floor: {floor}",
            color=cf.getRandomColor(),
        )
        log.debug(f"Created Embed")

        log.debug(f"Assigning Values")
        statsData = data_tuple[0]
        bestRun = data_tuple[1]

        statsDataString = f"```\nTimes Played: {statsData[0]}\nBest Total Score: {statsData[1]}\nTotal Mobs Killed: {statsData[2]}\nMost Mobs Killed: {statsData[3]}\nCompleted Time (Minutes): {round(statsData[4], 2)}\nCompleted Time (Seconds): {round(statsData[5], 2)}```"
        bestRunString = f"```\nExploration: {bestRun[0]}\nSpeed: {bestRun[1]}\nSkill: {bestRun[2]}\nBonus: {bestRun[3]}\nDamage Dealt: {bestRun[5]}\nDeaths: {bestRun[6]}\nMobs Killed: {bestRun[7]}\nSecrets Found: {bestRun[8]}```"

        teammatesString = "```"
        i = 1
        for teammate in bestRun[4]:
            teammatesString = teammatesString + str(i) + ". " + teammate + "\n"
            i += 1
        teammatesString += "```"

        log.debug(f"Assigned Values")
        log.debug(f"Adding Fields to Embed")

        embed.add_field(name="Stats", value=statsDataString, inline=False)
        embed.add_field(name="Best Run", value=bestRunString, inline=False)
        embed.add_field(
            name="Teammates for Best Run", value=teammatesString, inline=False
        )

        log.debug(f"Added Fields to Embed")

        log.debug(f"Sending Embed")
        await ctx.send(embed=embed)
        log.debug(f"Sent Embed")

    # Errors
    @floor.error
    async def floor_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(
                f"Please Send a Username and a Floor Number Along With the Command"
            )

        if isinstance(error, Exception):
            await ctx.send(f"Username not Found")


def setup(client):
    client.add_cog(Dungeon(client))


# https://hypixel-api.senither.com/v1/profiles/e2deec36-7d8c-4ddb-92fe-8507dbdbdd33/latest/?key=7c8ec3eb-6d72-42a6-8795-675a4b673001


def floorData(username, floor):
    log.info(f"floorData called for {username} on floor {floor}")

    log.debug(f"Requesting Latest Profile")
    _, profile_id = cf.getLatestProfile(cf.getUUID(username))
    log.debug(f"Received Latest Profile")

    log.debug(f"Requesting Data")
    fD = get(f"https://sky.shiiyu.moe/api/v2/profile/{username}/").json()["profiles"][
        profile_id
    ]["data"]["dungeons"]["catacombs"]["floors"][str(floor)]
    log.debug(f"Received Data")

    log.debug(f"Assigning Stats Data")
    statData = fD["stats"]

    timesPlayed = statData["times_played"]
    bestScore = statData["best_score"]
    totalMobsKilled = statData["mobs_killed"]
    mostMobsKilled = statData["most_mobs_killed"]
    completedTimeMS = statData["fastest_time"]
    completedTimeS = round(completedTimeMS / 1000, 2)
    completedTimeM = round(completedTimeMS / (1000 * 60), 0)
    # classSelected = formatClass(statData["dungeon_class"]) # Removed from API
    log.debug(f"Assigned Stats Data")

    log.debug(f"Assigning Best Run Data")
    bestRunData = fD["best_runs"][0]

    explorationB = bestRunData["score_exploration"]
    speedB = bestRunData["score_speed"]
    skillB = bestRunData["score_skill"]
    bonusB = bestRunData["score_bonus"]

    teammates = bestRunData["teammates"]
    teammatesConverted = cf.convertTeammates(teammates)

    damageDealt = round(bestRunData["damage_dealt"], 2)
    deaths = bestRunData["deaths"]
    mobs_killed = bestRunData["mobs_killed"]
    secrets_found = bestRunData["secrets_found"]
    log.debug(f"Finished Assigning Values")

    stats = [
        timesPlayed,
        bestScore,
        totalMobsKilled,
        mostMobsKilled,
        completedTimeM,
        completedTimeS,
        # classSelected, # Removed from API
    ]
    bestRun = [
        explorationB,
        speedB,
        skillB,
        bonusB,
        teammatesConverted,
        num.comma(damageDealt),
        deaths,
        mobs_killed,
        secrets_found,
    ]

    log.debug(f"Returning Lists")
    return stats, bestRun


# print(floorData("nottcurious", 0))
# # print(get('https://sky.shiiyu.moe/api/v2/profile/NottCurious').json()['profiles'])


def formatClass(classRaw):
    return classRaw.capitalize()


if __name__ == "__main__":
    print(floorData(username="NottCurious", floor=1))
    print(floorData(username="NottCurious", floor=2))
    print(floorData(username="NottCurious", floor=3))
    print(floorData(username="NottCurious", floor=4))
    print(floorData(username="NottCurious", floor=5))
    print(floorData(username="NottCurious", floor=6))
    print(floorData(username="NottCurious", floor=7))
