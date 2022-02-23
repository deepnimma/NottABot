import discord
from discord.ext import commands
import logging
import os
from dotenv import load_dotenv
from math import sqrt

try:
    import cogs.convertLogging as cl
except:
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
    embed = discord.Embed(
        title=f"We're Working on {ctx.command}, Please Wait...",
        color=cf.getRandomColor(),
    )

    await ctx.send(embed=embed, delete_after=2)


async def finish_usage(self, ctx):
    log.info(f"{ctx.author} finished using {ctx.command} in {ctx.guild}")


class QuickMaths(commands.Cog, name="Maths", description="Math Functions"):
    def __init__(self, client):
        self.client = client

    # Commands
    @commands.command(
        help="Shows Factorial of the Given Number", brief="Factorial of Number"
    )
    @commands.before_invoke(record_usage)
    @commands.after_invoke(finish_usage)
    async def fact(self, ctx, num: int):
        embed = discord.Embed(title=f"Factorial of {num}", color=cf.getRandomColor())
        embed.add_field(name=f"Factorial", value=f"{factorial(num)}", inline=False)

        await ctx.send(embed=embed)

    @commands.command(
        help="Shows Square Root of the Given Number", brief="Root of a Number"
    )
    @commands.before_invoke(record_usage)
    @commands.after_invoke(finish_usage)
    async def root(self, ctx, num: float):
        embed = discord.Embed(title=f"Square Root of {num}", color=cf.getRandomColor())
        embed.add_field(
            name=f"Square Root", value=f"{round(returnSQRT(num), 5)}", inline=False
        )

        await ctx.send(embed=embed)

    @commands.command(help="(a ^ b) % mod")
    @commands.before_invoke(record_usage)
    @commands.after_invoke(finish_usage)
    async def getpow(self, ctx, num: float, power: int, modulus: float = 1e9 + 7):
        embed = discord.Embed(
            title=f"Power of {num} to {power} with Modulus {modulus}",
            color=cf.getRandomColor(),
        )
        embed.add_field(
            name=f"Power", value=f"{round((num ** power) % modulus, 5)}", inline=False
        )

        await ctx.send(embed=embed)

    # Errors


def setup(client):
    client.add_cog(QuickMaths(client))


def factorial(num: int):
    log.debug(f"Factorial called for {num}")
    if num <= 1:
        return 1
    else:
        return num * factorial(num - 1)


def returnSQRT(num: float):
    log.debug(f"Returning Square Root of {num}")
    return sqrt(num)
