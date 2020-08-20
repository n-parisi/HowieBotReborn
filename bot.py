import os
from discord.ext import commands

from cogs.pics import Pics
from cogs.sounds import Sounds

# create bot
bot = commands.Bot(command_prefix='!')

# attach cogs
bot.add_cog(Sounds(bot))
bot.add_cog(Pics(bot))

# start bot
bot.run(os.environ['DISCORD_BOT_TOKEN'])
