import os
import random

import discord
from discord.ext import commands

from pkg.utils.aws_utils import sync_resources
from pkg.utils.config import cfg

RESOURCE_PATH = 'resources/pics/'


class Pics(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        if cfg['use_aws_resources']:
            sync_resources(cfg['bucket_name'], cfg['pics_prefix'], RESOURCE_PATH)

    @commands.command()
    async def pic(self, ctx):
        file_name = random.choice(os.listdir(RESOURCE_PATH))
        await ctx.send(file=discord.File(RESOURCE_PATH + file_name))

    @commands.command()
    async def picBurst(self, ctx, count):
    	x = count
    	while x < count: 
        	file_name = random.choice(os.listdir(RESOURCE_PATH))
        	await ctx.send(file=discord.File(RESOURCE_PATH + file_name))
        	x += 1
