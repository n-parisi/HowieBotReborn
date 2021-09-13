import os

from discord.ext import commands

from pkg.cogs.pics import Pics
from pkg.cogs.sounds import Sounds
from pkg.cogs.wager import Wagers

# create bot
bot = commands.Bot(command_prefix='!', help_command=None)

# attach cogs
bot.add_cog(Sounds(bot))
bot.add_cog(Pics(bot))
bot.add_cog(Wagers(bot))


# TODO: Use built in help command instead of...this
@bot.command()
async def help(ctx, subhelp=None):
    if subhelp == 'newclip':
        await ctx.send('```!newclip youtube.com/abc 00:05:30.00 10\n'
                       '    Creates a new clip that begins at the 5 min 30 sec mark in the video, and runs for 10 seconds\n'
                       '!play test\n'
                       '    Listen to the created clip.\n'
                       '!saveclip testclip\n'
                       '    Save it as a new clip called testclip.```')
    elif subhelp == 'playlist':
        await ctx.send('```!playlist clip 1, clip 2, clip 3, 5\n'
                       '    Play the listed clips in sequence, with a delay of 5 seconds between each.\n'
                       '!playlist 5\n'
                       '    Plays 3 random clips with a 5 second delay between each.```')
    elif subhelp == 'delay':
        await ctx.send('```!delay clip 1, clip 2, clip 3, 500\n'
                       '    Creates a new clip from overlaying each clip every 500ms.\n'
                       '!delay 500\n'
                       '    Creates a new clip from overlaying 5 random clips every 500ms.```')
    else:
        await ctx.send('```Available Commands: \n'
                       '   !pic                 Share a random Howie Pic\n'
                       '   !play                Play a random sound clip\n'
                       '   !clips               List all clips\n'
                       '   !play <clip name>    Play a specific sound clip\n'
                       '   !newclip             Create a new clip. "!help newclip" for more\n'
                       '   !playlist            Play a lit of clips. "!help playlist" for more\n'
                       '   !delay               Overlay clips after a delay. "!help delay" for more```')


@bot.command()
async def build(ctx):
    if 'BUILD_ID' in os.environ:
        build_id = os.environ['BUILD_ID']
        build_str = f'{build_id}'
    else:
        build_str = "undefined"
    await ctx.send(build_str)


@bot.command()
async def servers(ctx):
    servers = list(bot.guilds)
    await ctx.send(f"Connected on {str(len(servers))} servers:")
    await ctx.send('\n'.join(guild.name for guild in servers))


@bot.command()
async def unstuck(ctx):
    for client in bot.voice_clients:
        await client.disconnect(force=True)

# start bot
print("Starting bot!")
bot.run(os.environ['DISCORD_BOT_TOKEN'])
