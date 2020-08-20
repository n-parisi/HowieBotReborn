import asyncio
import os
import random

import discord
from discord.ext import commands


class Pics(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def pic(self, ctx):
        file_name = random.choice(os.listdir("resources/pics"))
        await ctx.send(file=discord.File("resources/pics/" + file_name))
