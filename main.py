import os

from discord.ext import commands

from pkg.cogs.pics import Pics
from pkg.cogs.sounds import Sounds
from pkg.cogs.wordcloud import WordCloud

# create bot
bot = commands.Bot(command_prefix='!', help_command=None)

# attach cogs
bot.add_cog(Sounds(bot))
bot.add_cog(Pics(bot))
bot.add_cog(WordCloud(bot))


# add help command
@bot.command()
async def help(ctx):
    await ctx.send('```Available Commands: \n'
                   '   !pic                 Share a random Howie Pic\n'
                   '   !play                Play a random sound clip\n'
                   '   !sounds              List all clips\n'
                   '   !play <clip name>    Play a specific sound clip\n'
                   '   !wordcloud 5000      Create wordcloud for last X messages (limit 10000)```')


# start bot
print("Starting bot!")
bot.run(os.environ['DISCORD_BOT_TOKEN'])
