import os

from discord.ext import commands

from pkg.cogs.pics import Pics
from pkg.cogs.sounds import Sounds

# create bot
bot = commands.Bot(command_prefix='!', help_command=None)

# attach cogs
bot.add_cog(Sounds(bot))
bot.add_cog(Pics(bot))


# add help command
@bot.command()
async def help(ctx):
    await ctx.send('```Available Commands: \n'
                   '   !pic                 Share a random Howie Pic\n'
                   '   !play                Play a random sound clip\n'
                   '   !sounds              List all clips\n'
                   '   !play <clip name>    Play a specific sound clip```')


@bot.command()
async def build(ctx):
    if os.environ['TRAVIS']:
        build_id = os.environ['TRAVIS_BUILD_ID']
        build_num = os.environ['TRAVIS_BUILD_NUMBER']

        build_id = f'{build_id}---build:{build_num}'
    else:
        build_id = "local"
    await ctx.send(build_id)


# start bot
print("Starting bot!")
bot.run(os.environ['DISCORD_BOT_TOKEN'])
