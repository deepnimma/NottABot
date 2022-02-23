import discord
from discord.ext import commands
import logging
import os
from dotenv import load_dotenv

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
    embed = discord.Embed(
        title=f"We're Working on {ctx.command}, Please Wait...",
        color=cf.getRandomColor(),
    )

    await ctx.send(embed=embed, delete_after=2)


async def finish_usage(self, ctx):
    log.info(f"{ctx.author} finished using {ctx.command} in {ctx.guild}")


class Moderation(commands.Cog, description="Moderation Functions"):
    def __init__(self, client):
        self.client = client

    # Commands
    @commands.command(
        aliases=["purge"],
        help="Clears Given Amount of Messages from Channel",
        brief="Clears Messages",
    )
    @commands.before_invoke(record_usage)
    @commands.after_invoke(finish_usage)
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int):
        await ctx.channel.purge(limit=amount)
        log.debug(f"Cleared {amount} messages")

        log.debug(f"Creating Embed")
        embed = discord.Embed(
            title=f"Cleared {amount} message(s) from {ctx.channel}", color=0xFF0000
        )
        log.debug(f"Created Embed")

        log.debug(f"Sending Embed")
        await ctx.send(embed=embed, delete_after=4)
        log.debug(f"Sent Embed")

    @commands.command(help="Kicks Given Member from the Server")
    @commands.before_invoke(record_usage)
    @commands.after_invoke(finish_usage)
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        await member.kick(reason=reason)
        log.debug(f"Kicked {member}")

        log.debug(f"Creating Embed")
        embed = discord.Embed(title=f"Kicked {member}", color=0xFF0000)
        log.debug(f"Created Embed")

        log.debug(f"Sending Embed")
        await ctx.send(embed=embed, delete_after=4)
        log.debug(f"Sent Embed")

    @commands.command(help="Bans Given Member from the Server")
    @commands.before_invoke(record_usage)
    @commands.after_invoke(finish_usage)
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        await member.ban(reason=reason)
        log.debug(f"Banned {member}")

        log.debug(f"Creating Embed")
        embed = discord.Embed(title=f"Banned {member}", color=0xFF0000)
        log.debug(f"Created Embed")

        log.debug(f"Sending Embed")
        await ctx.send(embed=embed, delete_after=4)
        log.debug(f"Sent Embed")

    @commands.command(help="Unbans Given Member from the Server")
    @commands.before_invoke(record_usage)
    @commands.after_invoke(finish_usage)
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member):
        log.debug("Requesting Ban List")
        banned_users = await ctx.guild.bans()
        log.debug("Received Ban List")

        log.debug("Splitting Given Username")
        member_name, member_discriminator = member.split("#")

        for ban_entry in banned_users:
            user = ban_entry.user

            log.debug(f"Checking {user} for {ctx.guild}")
            if (user.name, user.discriminator) == (member_name, member_discriminator):
                log.debug("User Found in Ban List")

                await ctx.guild.unban(user)

                log.debug(f"[Successful] - Creating Embed")
                embed = discord.Embed(title=f"Unbanned {user}", color=0xFF0000)
                log.debug(f"[Successful] - Created Embed")

                log.debug(f"[Successful] - Sending Embed")
                await ctx.send(embed=embed, delete_after=4)
                log.debug(f"[Successful] - Sent Embed")
                return

        log.critical(f"User: {member} is not found in Ban List")

        log.debug(f"[Unsuccessful] - Creating Embed")
        embed = discord.Embed(title=f"User Not Found in Ban List", color=0xFF0000)
        log.debug(f"[Unsuccessful] - Created Embed")

        log.debug(f"[Unsuccessful] - Sending Embed")
        await ctx.send(embed=embed, delete_after=4)
        log.debug(f"[Unsuccessful] - Sent Embed")

    # Errors
    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please Enter the Amount of Messages to Delete")
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(
                "You Are Missing the Permissions Required for This Command (Manage Messages Permission)"
            )

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(
                "You Do Not Have the Required Role for this Command (Kick Members)"
            )
        if isinstance(error, commands.errors.CommandInvokeError):
            await ctx.send("You Cannot Kick Someone With a Higher Role Priority")
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please Tag a Person To Kick")

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(
                "You Do Not Have the Required Role for this Command (Ban Members)"
            )
        if isinstance(error, commands.errors.CommandInvokeError):
            await ctx.send("You Cannot Ban Someone With a Higher Role Priority")
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please Tag a Person To Ban")

    @unban.error
    async def unban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(
                "You Do Not Have the Required Role for this Command (Ban Members)"
            )
        if isinstance(error, commands.errors.CommandInvokeError):
            await ctx.send("You Cannot Ban Someone With a Higher Role Priority")
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please Tag a Person To Ban")
        if isinstance(error, ValueError):
            await ctx.send("Invalid Name Format")


def setup(client):
    client.add_cog(Moderation(client))
