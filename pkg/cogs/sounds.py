import asyncio
import os
import random

import discord
from discord.ext import commands

from pkg.utils.aws_utils import sync_resources
from pkg.utils.config import cfg

RESOURCE_PATH = 'resources/sounds/'


class Sounds(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        if cfg['use_aws_resources']:
            sync_resources(cfg['bucket_name'], cfg['sounds_prefix'], RESOURCE_PATH)

    @commands.command()
    async def play(self, ctx, *, sound='random'):
        user = ctx.message.author
        # only play sound if user is in a voice channel
        if user.voice is not None:
            all_sounds = get_sounds()
            channel = user.voice.channel
            if sound == 'random':
                random_sound = random.choice(all_sounds)
                await play_sound(channel, random_sound)
            elif sound in all_sounds:
                await play_sound(channel, sound)

    @commands.command()
    async def sounds(self, ctx):
        result_str = ", ".join(sorted(get_sounds()))
        await ctx.send(result_str[:-2])

    @commands.command()
    async def delay(self, ctx, *, time=500, amount=5, sound='random'):
        user = ctx.message.author
        # only play sound if user is in a voice channel
        if user.voice is not None:
            all_sounds = get_sounds()
            channel = user.voice.channel
            if sound == 'random':
                random_sound = random.choice(all_sounds)
                await play_sound_loop(channel, time, amount, random_sound)
            elif sound in all_sounds:
                await play_sound_loop(channel, time, amount, sound)


async def play_sound(channel, sound):
    voice_client = await channel.connect()
    source = discord.FFmpegPCMAudio(get_sound_file(sound))
    voice_client.play(source)
    while voice_client.is_playing():
        await asyncio.sleep(1)
    await voice_client.disconnect()

async def play_sound_loop(channel, time, amount, sound):
    voice_client = await channel.connect()
    source = discord.FFmpegPCMAudio(get_sound_file(sound))
    i = 0
    while i < amount:
    	voice_client.play(source)
    	i += 1
   		while voice_client.is_playing():
       		await asyncio.sleep(time)

    await voice_client.disconnect()



def get_sounds():
    return [filename[:filename.index(".")] for filename in os.listdir(RESOURCE_PATH)]


def get_sound_file(sound):
    for filename in os.listdir(RESOURCE_PATH):
        if sound in filename:
            return RESOURCE_PATH + filename
