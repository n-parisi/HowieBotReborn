from discord.ext import commands
from pkg.cogs.sounds import get_clips, to_int
import pkg.utils.db_utils as db_utils
from pkg.utils.config import cfg


class Wagers(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def wager(self, ctx, *, arg):
        args = arg.split(',')
        amount, clip, count = args[0], args[1], args[2]
        # get users account
        user = ctx.message.author
        howie_account = db_utils.get_account(user.id)
        if howie_account is None:
            howie_account = db_utils.new_account(user.id, user.display_name)
            await ctx.send(f"New HowieBucks account created for user {user.display_name}.")
        # perform validations
        clip = clip.strip()
        if amount[0] != '$' or to_int(amount[1:]) < 0:
            await ctx.send("Wager should be amount starting with '$'")
        elif to_int(amount[1:]) > howie_account['bucks']:
            await ctx.send("You don't have enough HowieBucks to place this wager")
        elif clip not in get_clips():
            await ctx.send("Clip does not exist.")
        elif to_int(count) == -1:
            await ctx.send("Last value must be number")
        else:
            db_utils.new_wager(user.display_name, howie_account, to_int(amount[1:]), clip, to_int(count))
            await ctx.send("Wager placed.")

    @commands.command()
    async def bucks(self, ctx):
        results = db_utils.get_accounts()
        results.sort(key=lambda x: x['bucks'], reverse=True)

        results_str = ""
        for result in results:
            results_str += f"{result['name']} --- ${format(result['bucks'], '.2f')}\n"
        await ctx.send(results_str if len(results_str) > 0 else "None")

    @commands.command()
    async def wagers(self, ctx, user=None):
        results = db_utils.get_wagers(user)
        results.sort(key=lambda x: x['disp_name'])

        results_str = ""
        for result in results:
            pay_out = format(result['amount'] + result['amount'] * len(get_clips()) / result['start_count'], '.2f')
            results_str += f"{result['disp_name']} --- {result['clip']} --- Bet: ${result['amount']} --- Payout: ${pay_out}" \
                           f"--- {result['count']} / {result['start_count']} attempts left\n"
            if len(results_str) > 1700:
                await ctx.send(results_str if len(results_str) > 0 else "None")
                results_str = ""
        await ctx.send(results_str if len(results_str) > 0 else "None")

    @commands.command()
    async def winners(self, ctx, arg=None, arg2=None):
        if arg is None or to_int(arg) > -1:
            arg = 50 if arg is None else to_int(arg)
            results = db_utils.get_win_records()
            results.reverse()
            results = results[:arg]
        else:
            arg2 = 50 if arg2 is None else to_int(arg2)
            results = db_utils.get_win_records(arg)
            results.reverse()
            results = results[:arg2]

        results_str = ''
        for result in results:
            results_str += f"{result['disp_name']} won ${format(result['amount'], '.2f')} for {result['clip']}\n"
            if len(results_str) > 1700:
                await ctx.send(results_str)
                results_str = ""
        await ctx.send(results_str if len(results_str) > 0 else "None")

    @commands.command()
    async def bigwins(self, ctx, arg=None):
        if arg is None or to_int(arg) > -1:
            arg = 25 if arg is None else to_int(arg)
            results = db_utils.get_win_records()
            results.sort(key=lambda x: x['amount'], reverse=True)
            results = results[:arg]
        else:
            results = db_utils.get_win_records(arg)
            results.sort(key=lambda x: x['amount'], reverse=True)
            results = results[:10]

        results_str = ''
        for result in results:
            results_str += f"{result['disp_name']} won {format(result['amount'], '.2f')} for {result['clip']}\n"
            if len(results_str) > 1700:
                await ctx.send(results_str)
                results_str = ""
        await ctx.send(results_str if len(results_str) > 0 else "None")

    @commands.command()
    async def freemoney(self, ctx, amt, user_id=None):
        if ctx.message.author.id == cfg['admin_id']:
            db_utils.add_bucks(to_int(amt), to_int(user_id) if user_id is not None else None)
