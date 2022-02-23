import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
from requests import get
import logging
import time
import asyncio
import youtube_dl
import json

try:
    import cogs.commonFunctions as cf
    import cogs.numberformat as num
except:
    import commonFunctions as cf
    import numberformat as num

load_dotenv()
api_key = os.getenv('APIKEY')\
log_level = os.getenv('LOGLEVEL')
discord_log_level = os.getenv('DISCORD_LOG_LEVEL')

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



youtube_dl.utils.bug_reports_message = lambda: ''

f = open('./Data/Options/ytdl.json')
ytdl_format_options = json.load(f)
f.close()
f = open('./Data/Options/ffmpeg.json')
ffmpeg_options = json.load(f)
f.close()


ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


class Music(commands.Cog, name='Music', description='Music Player Commands'):
    def __init__(self, client):
        self.client = client

    @commands.command(help='Joins the Given Voice Channel')
    @commands.before_invoke(record_usage)
    @commands.after_invoke(finish_usage)
    async def join(self, ctx, url_: str) -> None:
        