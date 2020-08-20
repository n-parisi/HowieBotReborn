import asyncio
import os
import random

import discord
from discord.ext import commands


class Sounds(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

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
        result_str = ''
        for sound in sorted(get_sounds()):
            result_str += sound + ', '
        await ctx.send(result_str[:-2])


async def play_sound(channel, sound):
    voice_client = await channel.connect()
    source = discord.FFmpegPCMAudio(get_sound_file(sound))
    voice_client.play(source)
    while voice_client.is_playing():
        await asyncio.sleep(1)
    await voice_client.disconnect()


def get_sounds():
    return [filename[:filename.index(".")] for filename in os.listdir("resources/sounds")]


def get_sound_file(sound):
    for filename in os.listdir("resources/sounds"):
        if sound in filename:
            return "resources/sounds/" + filename
