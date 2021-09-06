import asyncio
import os
import random
import re

import discord
from discord.ext import commands

from pkg.utils.discord_utils import is_admin_request
import pkg.utils.aws_utils as aws
from pkg.utils.clip_utils import create_clip, splice_clips
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
    async def playlist(self, ctx, *, arg):
        user = ctx.message.author
        # only play sound if user is in a voice channel
        if user.voice is not None:
            all_sounds = get_clips()
            channel = user.voice.channel

            args = arg.split(',')
            # last arg needs to be a number
            delay = to_int(args[-1])
            if delay < 0 or delay > 10:
                await ctx.send('Last parameter needs to be a number in seconds, less than 10')
            # if delay is the only parameter, play 3 random sounds
            elif len(args) == 1:
                sounds = [random.choice(all_sounds) for i in range(3)]
                await play_clips_delay(channel, sounds, delay)
            else:
                sounds = args[0:-1]
                await play_clips_delay(channel, sounds, delay)

    @commands.command()
    async def delay(self, ctx, *, arg):
        user = ctx.message.author
        # only play sound if user is in a voice channel
        if user.voice is not None:
            all_sounds = get_clips()
            channel = user.voice.channel

            args = arg.split(',')
            # last arg needs to be a number
            delay = to_int(args[-1])
            sounds = None
            if delay < 0 or delay > 5000:
                await ctx.send('Last parameter needs to be a number in milliseconds, less than 5000')
            # if delay is the only parameter, splice 5 random sounds
            elif len(args) == 1:
                sounds = [get_clip_file(random.choice(all_sounds)) for i in range(5)]
            else:
                user_sounds = args[0:-1]
                # replace any use of the word 'random' with a random clip
                # user_sounds = map(lambda sound: random.choice(all_sounds) if sound == 'random' else sound, user_sounds)
                # Validate all provided sounds
                valid = True
                for user_sound in user_sounds:
                    user_sound = user_sound.strip()
                    if user_sound not in all_sounds:
                        valid = False
                if not valid:
                    await ctx.send('Invalid list of clips provided.')
                else:
                    sounds = [get_clip_file(sound.strip()) for sound in user_sounds]

            if not sounds is None:
                await ctx.send('Splicing a new audio clip...')
                splice_clips(sounds, delay)
                await ctx.send('New clip created. `!play test` to hear it again, `!saveclip clip_name` to save it.')
                await play_clip(channel, 'resources/tmp.mp3')            

    @commands.command()
    async def clips(self, ctx):
        clip_list_msg = ''
        for clip_name in sorted(get_clips()):
            clip_list_msg += clip_name
            # Break up message every 1500 chars (Discord limit is 2000 per message)
            if len(clip_list_msg) > 1500:
                await ctx.send(clip_list_msg)
                # Start building a new message
                clip_list_msg = ''
            else:
                clip_list_msg += ', '
        await ctx.send(clip_list_msg)

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
            await ctx.send('Creating clip...')
            create_clip(yt_link, start, duration_str, 'resources/tmp.mp3')
            await ctx.send('New clip created. `!play test` to hear it again, `!saveclip clip_name` to save it.')

            # Could be refactored
            voice = ctx.message.author.voice
            if voice is not None:
                await play_clip(voice.channel, 'resources/tmp.mp3')

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

    @commands.command()
    async def savefile(self, ctx):
        if not cfg['allow_savefile']:
            await ctx.send('Save file command is disabled.')
        if is_admin_request(ctx) and len(ctx.message.attachments) > 0:
            attachment = ctx.message.attachments[0]
            file_name = attachment.filename
            file_extension = file_name[file_name.index("."):]

            if file_name[:file_name.index(".")] in get_clips():
                await ctx.send('Clip with that name already exists.')
            elif (file_extension != '.wav') and (file_extension != '.mp3'):
                await ctx.send('Invalid file, must be .wav or .mp3.')
            else:
                print(f"Saving attachment...{file_name}")
                await attachment.save(RESOURCE_PATH + file_name)
                aws.save_resource(cfg['bucket_name'], RESOURCE_PATH + file_name)
                await ctx.send('File saved!')


async def play_clip(channel, sound_file):
    voice_client = await channel.connect()
    source = discord.FFmpegPCMAudio(sound_file)
    voice_client.play(source)
    while voice_client.is_playing():
        await asyncio.sleep(1)
    await voice_client.disconnect()

async def play_clips_delay(channel, sounds, delay):
    for i in range(len(sounds)):
        sound = sounds[i].strip()
        await play_clip(channel, get_clip_file(sound))
        if not i == len(sounds) - 1:
            await asyncio.sleep(delay)

def get_clips():
    return [filename[:filename.index(".")] for filename in os.listdir(RESOURCE_PATH)]


def get_clip_file(sound):
    for filename in os.listdir(RESOURCE_PATH):
        if sound == filename[0:-4]:
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

def to_int(s):
    try:
        return int(s)
    except ValueError:
        return -1
