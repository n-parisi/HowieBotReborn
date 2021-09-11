import os
import random

import discord
from discord.ext import commands

import pkg.utils.db_utils as wager_utils


class Wagers(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def wager(self, ctx):
        user = ctx.message.author
        wager_utils.new_account(user.id, user.display_name)

    @commands.command()
    async def howiebucks(self, ctx):
        results = wager_utils.get_accounts()
        await ctx.send(str(results))
