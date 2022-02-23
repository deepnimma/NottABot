import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
from requests import get
import logging
import time
from math import floor

try:
    import cogs.numberformat as num
    from cogs.numberformat import comma
    import cogs.commonFunctions as cf
    import cogs.convertLogging as cl
except:
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


class HyCalc(
    commands.Cog,
    name="Hypixel Calculators",
    description="Calculation Related Functions",
):
    def __init__(self, client):
        self.client = client

    @commands.command(help="Shows 6 Enchanted Wood Prices", brief="Wood Prices")
    @commands.before_invoke(record_usage)
    @commands.after_invoke(finish_usage)
    async def woods(self, ctx):
        log.debug(f"Getting Wood Prices")
        wood_data = getWoodPrices()
        log.debug(f"Received Wood Prices")

        log.debug(f"Creating Embed")
        embed = discord.Embed(title="Wood Prices", color=cf.getRandomColor())

        embed.add_field(
            name="Enchanted Oak", value=f"```{wood_data[0]}```", inline=True
        )
        embed.add_field(
            name="Enchanted Birch", value=f"```{wood_data[1]}```", inline=True
        )
        embed.add_field(
            name="Enchanted Spruce", value=f"```{wood_data[2]}```", inline=True
        )
        embed.add_field(
            name="Enchanted Dark Oak", value=f"```{wood_data[3]}```", inline=True
        )
        embed.add_field(
            name="Enchanted Acacia", value=f"```{wood_data[4]}```", inline=True
        )
        embed.add_field(
            name="Enchanted Jungle", value=f"```{wood_data[5]}```", inline=True
        )
        log.debug(f"Created Embed")

        log.debug(f"Sending Embed")
        await ctx.send(embed=embed)
        log.debug(f"Sent Embed")

    @commands.command(
        help="Returns Price for 12, 18 or 29 Pot Splashes",
        brief="Splash Price for 12, 18 or 29",
    )
    @commands.before_invoke(record_usage)
    @commands.after_invoke(finish_usage)
    async def potprice(self, ctx, num: int = 12):
        log.debug(f"Pot Price for {num} Pots")

        allowed_nums = [12, 18, 29]

        if num not in allowed_nums:
            await ctx.send(f"That Number is Not Valid, Please Enter [12 | 18 | 29]")
            return

        log.debug(f"Calling Function for Data")
        data = getPotPrices(num)
        log.debug(f"Received Data from Function")

        log.debug(f"Creating Embed")
        embed = discord.Embed(
            title=f"Pot Prices for {num} Pots", color=cf.getRandomColor()
        )
        log.debug(f"Created Embed")

        log.debug(f"Adding Fields to Embed")

        embed.add_field(name="Pot Name", value=data[0], inline=False)
        embed.add_field(
            name="Number of Redstone Blocks and Glowstone Blocks",
            value=f"```{data[2]}```",
            inline=False,
        )
        embed.add_field(
            name="Price for 1 Set",
            value=f"```{comma(round(data[1], 2))}```",
            inline=False,
        )
        embed.add_field(
            name="Price for 3 Sets",
            value=f"```{comma(round(3 * data[1], 2))}```",
            inline=False,
        )

        log.debug(f"Added Fields to Embed")

        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(HyCalc(client))


def getWoodPrices():
    log.debug(f"Requesting Bazaar Data")
    bazaarData = get("https://sky.shiiyu.moe/api/v2/bazaar").json()
    log.debug(f"Received Bazaar Data")

    oak = round(bazaarData["ENCHANTED_OAK_LOG"]["buyPrice"], 2)
    birch = round(bazaarData["ENCHANTED_BIRCH_LOG"]["buyPrice"], 2)
    spruce = round(bazaarData["ENCHANTED_SPRUCE_LOG"]["buyPrice"], 2)
    dark_oak = round(bazaarData["ENCHANTED_DARK_OAK_LOG"]["buyPrice"], 2)
    acacia = round(bazaarData["ENCHANTED_ACACIA_LOG"]["buyPrice"], 2)
    jungle = round(bazaarData["ENCHANTED_JUNGLE_LOG"]["buyPrice"], 2)

    log.debug(f"Returning Tuple")
    return (oak, birch, spruce, dark_oak, acacia, jungle)


def getPotPrices(num):
    if num == 12:
        return getPotPrices12()
    elif num == 18:
        return getPotPrices18()
    elif num == 29:
        return getPotPrices29()


def getPotPrices12():
    pot_names = (
        "Speed",
        "Strength",
        "Rabbit",
        "Adrenaline",
        "Critical",
        "Agility",
        "Experience",
        "Haste",
        "Archery",
        "True Resistance",
        "Pet Luck",
        "Dodge",
    )
    pot_material_ids = (
        "ENCHANTED_SUGAR_CANE",
        "ENCHANTED_BLAZE_ROD",
        "ENCHANTED_RABBIT_FOOT",
        "ENCHANTED_COOKIE",
        "FLINT",
        "ENCHANTED_CAKE",
        "INK_SACK:4",
        "COAL",
        "FEATHER",
        "ENCHANTED_RABBIT_HIDE",
        "RAW_FISH:1",
    )

    num_blocks = len(pot_names) / 3

    log.debug(f"Requesting Bazaar Data")
    bazaar_data = get("https://sky.shiiyu.moe/api/v2/bazaar").json()
    log.debug(f"Received Bazaar Data")

    log.debug(f"Changing Pot Names into String")
    pot_names_string = "```" + str(cf.makeString(pot_names)) + "```"
    log.debug(f"Changed Pot Names into String")

    cost = 25000

    log.debug(f"Adding Prices to Sum")
    for id in pot_material_ids:
        cost = cost + bazaar_data[id]["buyPrice"]
        log.debug(f"Current Cost is {cost}\r")
        time.sleep(0.0625)

    log.debug(f"Finding Glowstone and Redstone Prices")
    glowstone_price = num_blocks * (bazaar_data["ENCHANTED_GLOWSTONE"]["buyPrice"])
    redstone_price = num_blocks * bazaar_data["ENCHANTED_REDSTONE_BLOCK"]["buyPrice"]
    log.debug(f"Found Glowstone and Redstone Prices")

    cost = cost + glowstone_price + redstone_price

    log.debug(f"Returning Values")
    return (pot_names_string, round(cost, 2), num_blocks)


def getPotPrices18():
    pot_names = (
        "Speed",
        "Strength",
        "Rabbit",
        "Adrenaline",
        "Critical",
        "Agility",
        "Experience",
        "Haste",
        "Archery",
        "True Resistance",
        "Pet Luck",
        "Dodge",
        "Combat",
        "Fishing",
        "Foraging",
        "Farming",
        "Alchemy",
        "Enchanting",
    )
    pot_material_ids = (
        "ENCHANTED_SUGAR_CANE",
        "ENCHANTED_BLAZE_ROD",
        "ENCHANTED_RABBIT_FOOT",
        "ENCHANTED_COOKIE",
        "FLINT",
        "ENCHANTED_CAKE",
        "INK_SACK:4",
        "COAL",
        "FEATHER",
        "ENCHANTED_RABBIT_HIDE",
        "RAW_FISH:1",
    )

    num_blocks = len(pot_names) / 3

    log.debug(f"Requesting Bazaar Data")
    bazaar_data = get("https://sky.shiiyu.moe/api/v2/bazaar").json()
    log.debug(f"Received Bazaar Data")

    log.debug(f"Changing Pot Names into String")
    pot_names_string = "```" + str(cf.makeString(pot_names)) + "```"
    log.debug(f"Changed Pot Names into String")

    cost = 0

    log.debug(f"Adding Prices to Sum")
    for id in pot_material_ids:
        cost = cost + bazaar_data[id]["buyPrice"]
        log.debug(f"Current Cost is {cost}")

    log.debug(f"Finding Glowstone and Redstone Prices")
    glowstone_price = num_blocks * (bazaar_data["ENCHANTED_GLOWSTONE"]["buyPrice"])
    redstone_price = num_blocks * bazaar_data["ENCHANTED_REDSTONE_BLOCK"]["buyPrice"]
    log.debug(f"Found Glowstone and Redstone Prices")

    cost = cost + glowstone_price + redstone_price

    log.debug(f"Returning Values")
    return (pot_names_string, round(cost, 2), num_blocks)


def getPotPrices29():
    pot_names = (
        "Speed",
        "Strength",
        "Rabbit",
        "Adrenaline",
        "Critical",
        "Agility",
        "Experience",
        "Haste",
        "Archery",
        "True Resistance",
        "Pet Luck",
        "Dodge",
        "Combat",
        "Fishing",
        "Foraging",
        "Farming",
        "Alchemy",
        "Enchanting",
        "Water Breathing",
        "Fire Resistance",
        "Invisibility",
        "Regeneration",
        "Burning",
        "Stun",
        "Spelunker",
        "Absorption",
        "Stamina",
        "Mana",
        "Resistance",
    )
    pot_material_ids = (
        "ENCHANTED_SUGAR_CANE",
        "ENCHANTED_BLAZE_ROD",
        "ENCHANTED_RABBIT_FOOT",
        "ENCHANTED_COOKIE",
        "FLINT",
        "ENCHANTED_CAKE",
        "INK_SACK:4",
        "COAL",
        "FEATHER",
        "ENCHANTED_RABBIT_HIDE",
        "RAW_FISH:1",
        "ENCHANTED_PUFFERFISH",
        "MAGMA_CREAM",
        "SPIDER_EYE",
        "ENCHANTED_GHAST_TEAR",
        "SAND",
        "OBSIDIAN",
        "MITHRIL_ORE",
        "ENCHANTED_GOLD_BLOCK",
        "FOUL_FLESH",
        "ENCHANTED_COOKED_MUTTON",
        "ENCHANTED_CACTUS",
    )

    num_blocks = floor(len(pot_names) / 3)

    log.debug(f"Requesting Bazaar Data")
    bazaar_data = get("https://sky.shiiyu.moe/api/v2/bazaar").json()
    log.debug(f"Received Bazaar Data")

    log.debug(f"Changing Pot Names into String")
    pot_names_string = "```" + str(cf.makeString(pot_names)) + "```"
    log.debug(f"Changed Pot Names into String")

    cost = 0

    log.debug(f"Adding Prices to Sum")
    for id in pot_material_ids:
        cost = cost + bazaar_data[id]["buyPrice"]
        log.debug(f"Current Cost is {cost}")

    log.debug(f"Finding Glowstone and Redstone Prices")
    glowstone_price = num_blocks * (bazaar_data["ENCHANTED_GLOWSTONE"]["buyPrice"])
    redstone_price = num_blocks * bazaar_data["ENCHANTED_REDSTONE_BLOCK"]["buyPrice"]
    log.debug(f"Found Glowstone and Redstone Prices")

    cost = cost + glowstone_price + redstone_price

    log.debug(f"Returning Values")
    return (pot_names_string, round(cost, 2), num_blocks)


if __name__ == "__main__":
    print(getPotPrices12())
    print(getPotPrices18())
