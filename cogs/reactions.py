import discord
from discord.ext import commands
import logging
import os
from dotenv import load_dotenv
import random
import json

try:
    import cogs.commonFunctions as cf
    import cogs.convertLogging as cl
except:
    import commonFunctions as cf
    import convertLogging as cl

load_dotenv()
log_level = os.getenv("LOGLEVEL")
discord_log_level = os.getenv("DISCORD_LOG_LEVEL")

log = logging.getLogger(__name__)
log = cl.getLogging(log_level, discord_log_level)


async def record_usage(self, ctx):
    log.info(
        f"{ctx.author} used {ctx.command} at {ctx.message.created_at} in {ctx.guild}"
    )


async def finish_usage(self, ctx):
    log.info(f"{ctx.author} finished using {ctx.command} in {ctx.guild}")


class Reactions(commands.Cog, description="Reaction Functions"):
    def __init__(self, client):
        self.client = client

    # Commands
    @commands.command(help="Shows Crying Gif", brief="Cry")
    @commands.before_invoke(record_usage)
    @commands.after_invoke(finish_usage)
    async def cry(self, ctx):
        log.debug(f"Sending Embed")
        upperlim = 5
        newphrase = "***cries***"
        await ctx.send(
            embed=reactionFunction(
                lower=1, upper=upperlim, type="Cry", ctx=ctx, phrase=newphrase
            )
        )

    @commands.command(help="Shows Smug Gif", brief="Smug")
    @commands.before_invoke(record_usage)
    @commands.after_invoke(finish_usage)
    async def smug(self, ctx):
        log.debug(f"Sending Embed")
        upperlim = 7
        newphrase = "***is Smug!***"
        await ctx.send(
            embed=reactionFunction(
                lower=1, upper=upperlim, type="Smug", ctx=ctx, phrase=newphrase
            )
        )

    @commands.command(help="Shows Happy Gif", brief="Happy")
    @commands.before_invoke(record_usage)
    @commands.after_invoke(finish_usage)
    async def happy(self, ctx):
        log.debug(f"Sending Embed")
        upperlim = 8
        newphrase = "***is Happy!***"
        await ctx.send(
            embed=reactionFunction(
                lower=1, upper=upperlim, type="Happy", ctx=ctx, phrase=newphrase
            )
        )

    @commands.command(help="Shows Hug Gif", brief="Hug")
    @commands.before_invoke(record_usage)
    @commands.after_invoke(finish_usage)
    async def hug(self, ctx):
        log.debug(f"Sending Embed")
        upperlim = 5
        newphrase = "***Hugs!***"
        await ctx.send(
            embed=reactionFunction(
                lower=1, upper=upperlim, type="Hug", ctx=ctx, phrase=newphrase
            )
        )

    @commands.command(help="Shows Kissing Gif", brief="Kiss")
    @commands.before_invoke(record_usage)
    @commands.after_invoke(finish_usage)
    async def kiss(self, ctx):
        log.debug(f"Sending Embed")
        upperlim = 5
        newphrase = "***Kisses!***"
        await ctx.send(
            embed=reactionFunction(
                lower=1, upper=upperlim, type="Kiss", ctx=ctx, phrase=newphrase
            )
        )

    @commands.command(help="Shows Patting Gif", brief="Pat")
    @commands.before_invoke(record_usage)
    @commands.after_invoke(finish_usage)
    async def pat(self, ctx):
        log.debug(f"Sending Embed")
        upperlim = 5
        newphrase = "***Pats!***"
        await ctx.send(
            embed=reactionFunction(
                lower=1, upper=upperlim, type="Pat", ctx=ctx, phrase=newphrase
            )
        )

    @commands.command(help="Shows Shrug Gif", brief="Shrug")
    @commands.before_invoke(record_usage)
    @commands.after_invoke(finish_usage)
    async def shrug(self, ctx):
        log.debug(f"Sending Embed")
        upperlim = 5
        newphrase = "***Shrugs!***"
        await ctx.send(
            embed=reactionFunction(
                lower=1, upper=upperlim, type="Shrug", ctx=ctx, phrase=newphrase
            )
        )

    @commands.command(help="Shows Sleepy Gif", brief="Sleep")
    @commands.before_invoke(record_usage)
    @commands.after_invoke(finish_usage)
    async def sleepy(self, ctx):
        log.debug(f"Sending Embed")
        upperlim = 5
        newphrase = "***is Sleepy!***"
        await ctx.send(
            embed=reactionFunction(
                lower=1, upper=upperlim, type="Sleepy", ctx=ctx, phrase=newphrase
            )
        )

    @commands.command(help="Shows Triggered Gif", brief="Triggered")
    @commands.before_invoke(record_usage)
    @commands.after_invoke(finish_usage)
    async def triggered(self, ctx):
        log.debug(f"Sending Embed")
        upperlim = 4
        newphrase = "***is Triggered!***"
        await ctx.send(
            embed=reactionFunction(
                lower=1, upper=upperlim, type="Triggered", ctx=ctx, phrase=newphrase
            )
        )

    # Errors


def setup(client):
    client.add_cog(Reactions(client))


def getRandomInt(lower: int, upper: int):
    return random.randint(lower, upper)


def getRandomGif(type: str, num: int):
    linksNoJson = open(f"./Data/ReactionLinks/{type}.json")
    links = json.load(linksNoJson)

    links = links["links"]

    return links[num - 1]


def reactionFunction(lower: int, upper: int, type: str, ctx, phrase: str):
    log.debug(f"Retrieving Random Integer ({type})")
    randomint = getRandomInt(lower=lower, upper=upper)
    log.debug(f"Retrieved Random Chat ({type})")

    log.debug(f"Requesting Link ({type})")
    link = getRandomGif(type, randomint)
    log.debug(f"Requested Link ({type})")

    log.debug(f"Creating Embed ({type})")
    embed = discord.Embed(
        title=f"{ctx.message.author.mention} {phrase}",
        description="",
        color=cf.getRandomColor(),
    )
    embed.set_image(url=f"{link}")
    log.debug(f"Created Embed ({type})")

    log.debug(f"Returning Embed ({type})")
    return embed


if __name__ == "__main__":
    print(getRandomGif("Cry", 3))
