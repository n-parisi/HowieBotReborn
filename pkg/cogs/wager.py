import random

from discord.ext import commands
from discord import User, File
from pkg.cogs.sounds import get_clips, to_int
import pkg.utils.db_utils as db_utils
from pkg.utils.config import cfg

HOWIE_QUOTES = ["I am beloved by millions",
                "Please wash your tip before giving it to me",
                "oh sheit, im gonna nut." ,
                "Thanks for the tip budnut! Still not gonna play Gar!",
                "Thanks bud! All proceeds go to a fresh UN-RE for me!" ,
                "Oh shit thanks USER, Ill give you a sneaky here." ,
                "Whats your name again loser?",
                "What do you know skeetface?",
                "HAHA you call that a tip?",
                "Ive seen bigger tips on my dad" ,
                "HOWIEWOWIE now thats a tip!",
                "here's a tip for you, next roll is going to be RANDOMCLIPNAME",
                "Ill tell you whats NOT coming up next. Gar",
                "I have a gar in my pocket can you smell it?",
                "Back2Back JungleBoogie coming right up",
                "I have no peen",
                "Maybe you should stop betting. . .",
                "Maybe you should check out this jelqing manuel",
                "HowieHAPPY",
                "Have you seen the hit hidden camera show Mobbed?"]


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
            arg = 10 if arg is None else to_int(arg)
            results = db_utils.get_win_records()
            results.reverse()
            results = results[:arg]
        else:
            arg2 = 10 if arg2 is None else to_int(arg2)
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
            results_str += f"{result['disp_name']} won ${format(result['amount'], '.2f')} for {result['clip']}\n"
            if len(results_str) > 1700:
                await ctx.send(results_str)
                results_str = ""
        await ctx.send(results_str if len(results_str) > 0 else "None")

    @commands.command()
    async def tip(self, ctx, amount: int, mention: User = None):
        # get users account
        user = ctx.message.author
        howie_account = db_utils.get_account(user.id)
        if amount > howie_account['bucks'] or amount < 1:
            await ctx.send("You don't have enough HowieBucks to tip.")
        elif mention is not None:
            db_utils.add_tip(amount, howie_account, mention.id)
            await ctx.send(f"{user.name} just tipped {mention.name} ${amount}.")
        else:
            result = db_utils.add_tip(amount, howie_account)
            total_tips = result['total']
            howie_message = random.choice(HOWIE_QUOTES)\
                .replace("USER", howie_account["name"])\
                .replace("RANDOMCLIPNAME", random.choice(get_clips()))

            await ctx.send(f"{howie_message} --- I've been tipped ${total_tips}")
    
    
    @commands.command()
    async def tippers(self, ctx, arg=None):
        if arg is None:
            results = db_utils.get_tip_records()
            results.sort(key=lambda x: x['total'], reverse=True)
        else:
            results = db_utils.get_tip_records(arg)
        
        results_str = ''
        for result in results:
            results_str += f"{result['name']} has tipped ${format(result['total'], '.2f')}!\n"
            if len(results_str) > 1700:
                await ctx.send(results_str)
                results_str = ""
        await ctx.send(results_str if len(results_str) > 0 else "None")
        
        
    @commands.command()
    async def buystock(self, ctx, clip: str):
        # get users account
        user = ctx.message.author
        howie_account = db_utils.get_account(user.id)
        if howie_account['bucks'] < 200:
            await ctx.send("You need $200 to buy a stock.")
        elif clip not in get_clips():
            await ctx.send("Not a valid clip")
        else:
            db_utils.buy_stock(howie_account, clip)
            await ctx.send(f"{howie_account['name']} bought stock in {clip}")

    @commands.command()
    async def portfolio(self, ctx, user=None):
        if user is None:
            # get users account
            caller = ctx.message.author
            results = db_utils.get_stocks(caller.id)
        else:
            results = db_utils.get_stocks_by_disp(user)
        result_str = ''
        for result in results:
            result_str += f"{result['clip']} --- shares: {result['shares']} " \
                          f"--- total paid: ${format(result['total_payout'], '.2f')}\n"
        await ctx.send(result_str)

    @commands.command()
    async def freemoney(self, ctx, amt, user_id=None):
        if ctx.message.author.id == cfg['admin_id']:
            db_utils.add_bucks(to_int(amt), to_int(user_id) if user_id is not None else None)

            
    @commands.command()
    async def exportAll(self, ctx):
        results = db_utils.get_export();
        results.sort(key=lambda x: x['type'], reverse=True)
        with open('resources/exportAll.csv', 'w') as file:
            for result in results:
                jason_str = ""
                i = 0
                for thing in result:
                    if i == len(result) - 1:
                        jason_str += f"{thing}, {result[thing]}\n"
                    else:
                        jason_str += f"{thing}, {result[thing]}, "
                    i += 1
                file.write(jason_str)
        dataFile = File('resources/exportAll.csv')
        await ctx.send(file=dataFile, content="Exported database:\n")
        
        
    @commands.command()
    async def payout(self, ctx, arg=None):
        if arg is not None:
            results = db_utils.get_win_records_by_clip(arg)
            if len(results) > 0:
                sum = 0
                for result in results:
                    sum += result['amount']
                await ctx.send(f"{arg} has paid out ${format(sum, '.2f')} in wagers\n")
            else:
                if arg not in get_clips():
                    await ctx.send("Last value must be a valid clip name\n")
                else:
                    await ctx.send(f"{arg} has not paid out any wagers yet\n")  
            results = db_utils.get_stock_by_clip(arg)
            if len(results) > 0:
                sum = 0
                for result in results:
                    sum += result['total_payout']
                await ctx.send(f"{arg} has paid out ${format(sum, '.2f')} in stocks\n")
            else:
                if arg in get_clips():
                    await ctx.send(f"{arg} has not paid out any stocks yet\n")
        else:
            await ctx.send("Last value needs to be a clip name\n")
            
            
    @commands.command()
    async def lasthit(self, ctx, arg=None):
        if arg is None:
            await ctx.send("Enter a clip to check.")
        else:
            if arg in get_clips():
                result = db_utils.get_plays_counter(arg)
                if result is None:
                    await ctx.send(f"{arg} must play once before tracking can begin.")
                else:
                    await ctx.send(f"It has been {result['counter']} spins since {arg} has hit.")
            else:
                await ctx.send("Enter a valid clip to check.")