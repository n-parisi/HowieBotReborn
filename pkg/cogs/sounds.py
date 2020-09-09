import asyncio
import os
import random
import re

import discord
from discord.ext import commands

from pkg.utils.discord_utils import is_admin_request
import pkg.utils.aws_utils as aws
import pkg.utils.yt_utils as yt
from pkg.utils.config import cfg

RESOURCE_PATH = 'resources/sounds/'


class Sounds(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        if cfg['use_aws_resources']:
            aws.sync_resources(cfg['bucket_name'], cfg['sounds_prefix'], RESOURCE_PATH)

    @commands.command()
    async def play(self, ctx, *, sound='random'):
        user = ctx.message.author
        # only play sound if user is in a voice channel
        if user.voice is not None:
            all_sounds = get_clips()
            channel = user.voice.channel
            if sound == 'random':
                random_sound = random.choice(all_sounds)
                await play_clip(channel, get_clip_file(random_sound))
            elif sound == 'test':
                await play_clip(channel, 'resources/tmp.mp3')
            elif sound in all_sounds:
                await play_clip(channel, get_clip_file(sound))

    @commands.command()
    async def clips(self, ctx):
        result_str = ", ".join(sorted(get_clips()))
        await ctx.send(result_str[:-2])

    @commands.command()
    async def newclip(self, ctx, yt_link, start, duration_str):
        duration = to_float(duration_str)
        if not is_admin_request(ctx):
            await ctx.send('Clip creation only available to admins.')
        elif 'youtube.com' not in yt_link:
            await ctx.send('Clip must be a link to youtube.com.')
        elif not is_timestamp(start):
            await ctx.send('Start time must be in format HH:MM:SS.MM.')
        elif not 0 < duration <= 30:
            await ctx.send('Duration must be a number of seconds between 0 and 30.')
        else:
            yt.create_clip(yt_link, start, duration_str, 'resources/tmp.mp3')
            await ctx.send('New clip created. `!play test` to hear it, `!saveclip clip_name` to save it.')

    @commands.command()
    async def saveclip(self, ctx, clip_name):
        if is_admin_request(ctx):
            if clip_name not in get_clips():
                local_file = f'resources/sounds/{clip_name}.mp3'
                os.rename('resources/tmp.mp3', local_file)
                aws.save_resource(cfg['bucket_name'], local_file)
                await ctx.send("Clip created successfully!")
            else:
                await ctx.send("Clip with that name already exists.")


async def play_clip(channel, sound_file):
    voice_client = await channel.connect()
    source = discord.FFmpegPCMAudio(sound_file)
    voice_client.play(source)
    while voice_client.is_playing():
        await asyncio.sleep(1)
    await voice_client.disconnect()


def get_clips():
    return [filename[:filename.index(".")] for filename in os.listdir(RESOURCE_PATH)]


def get_clip_file(sound):
    for filename in os.listdir(RESOURCE_PATH):
        if sound in filename:
            return RESOURCE_PATH + filename


def is_timestamp(timestamp):
    if re.match(r'\d{2}:\d{2}:\d{2}\.\d{2}', timestamp) is None:
        return False
    else:
        return True


def to_float(s):
    try:
        return float(s)
    except ValueError:
        return -1
