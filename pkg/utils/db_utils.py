from tinydb import TinyDB, where
from tinydb.operations import subtract, set, decrement, add, increment
import uuid

db = TinyDB('resources/db.json')

STOCK_COST = 200
STOCK_PAYOUT = 10


def check_wagers(clip, total_clip_count):
    add_play_record(clip)
    is_wager = where('type') == 'wager'
    # decrease count of miss
    db.update(decrement('count'),
              is_wager & (where('clip') != clip))
    # delete the zeros
    db.remove(is_wager & (where('count') == 0))
    # get the hits
    results = db.search(is_wager & (where('clip') == clip))
    winners = []
    for result in results:
        # pay out
        pay_out = result['amount'] + result['amount'] * total_clip_count / result['start_count']
        db.update(add('bucks', pay_out),
                  (where('type') == 'account') & (where('id') == result['user_id']))
        # record win
        add_win_record((result['user_id'], result['disp_name'], clip, pay_out))
        # delete wager record
        db.remove(is_wager & (where('wager_id') == result['wager_id']))
        winners.append((result['disp_name'], pay_out, result['clip']))

    return winners


def check_stocks(clip):
    stocks = db.search((where('type') == 'stock') &
                       (where('clip') == clip))
    winners = []
    for stock in stocks:
        owner_id = stock['user_id']
        pay_out = STOCK_PAYOUT * stock['shares']
        db.update(add('bucks', pay_out),
                  (where('type') == 'account') & (where('id') == owner_id))
        db.update(add('total_payout', pay_out),
                  (where('type') == 'stock') &
                  (where('user_id') == owner_id) &
                  (where('clip') == clip))
        winners.append((stock['disp_name'], pay_out))
    return winners


def buy_stock(account, clip):
    # deduct the cost
    db.update(subtract('bucks', STOCK_COST),
              (where('type') == 'account') & (where('id') == account['id']))
    # purchase the stock
    if len(db.update(increment('shares'),
                     (where('type') == 'stock') &
                     (where('clip') == clip) &
                     (where('user_id') == account['id']))) == 0:
        db.insert({'type': 'stock',
                   'user_id': account['id'],
                   'disp_name': account['name'],
                   'clip': clip,
                   'shares': 1,
                   'total_payout': 0})


def add_bucks(amount, user_id=None):
    if user_id is None:
        db.update(add('bucks', amount),
                  where('type') == 'account')
    else:
        db.update(add('bucks', amount),
                  (where('type') == 'account') & (where('id') == user_id))


def add_play_record(clip):
    # increment if exists, otherwise create new record
    if len(db.update(increment('plays'),
                     (where('type') == 'play') & (where('clip') == clip))) == 0:
        db.insert({'type': 'play',
                   'clip': clip,
                   'plays': 1})


def add_tip(amt, account, send_to_id=None):
    # deduct amount
    db.update(subtract('bucks', amt),
              (where('type') == 'account') & (where('id') == account['id']))
    if send_to_id is not None:
        db.update(add('bucks', amt),
                  (where('type') == 'account') & (where('id') == send_to_id))
    elif len(db.update(add('total', amt),
                       (where('type') == 'tips'))) == 0:
        db.insert({'type': 'tips',
                   'total': amt})
    else:
        result = db.get(where('type') == 'tips')
        return result


def add_win_record(win_record):
    # win_record is (user_id, disp_name, clip, amt)
    db.insert({'type': 'win_record',
               'user_id': win_record[0],
               'disp_name': win_record[1],
               'clip': win_record[2],
               'amount': win_record[3]})


def new_account(discord_id, name):
    db.insert({'type': 'account',
               'id': discord_id,
               'name': name,
               'bucks': 100})
    return get_account(discord_id)


def new_wager(disp_name, account, amount, clip, count):
    # deduct amount
    db.update(subtract('bucks', amount),
              (where('type') == 'account') & (where('id') == account['id']))
    # update display name if needed
    db.update(set('name', disp_name),
              (where('type') == 'account') & (where('id') == account['id']))
    # place wager
    db.insert({'type': 'wager',
               'wager_id': str(uuid.uuid4()),
               'user_id': account['id'],
               'disp_name': disp_name,
               'clip': clip,
               'amount': amount,
               'count': count,
               'start_count': count})


def new_macro(macro_name, macro):
    db.insert({'type': 'macro',
               'name': macro_name,
               'macro': macro})


def get_macro(macro_name):
    result = db.search((where('type') == 'macro') & (where('name') == macro_name))
    return result[0] if len(result) > 0 else None


def get_accounts():
    return db.search(where('type') == 'account')


def get_account(discord_id):
    result = db.search((where('type') == 'account') & (where('id') == discord_id))
    return result[0] if len(result) > 0 else None


def get_wagers(user):
    if user is not None:
        return db.search((where('type') == 'wager') & (where('disp_name') == user))
    else:
        return db.search(where('type') == 'wager')


def get_plays(clip=None):
    if clip is not None:
        return db.get((where('type') == 'play') & (where('clip') == clip))
    else:
        results = db.search(where('type') == 'play')
        # sort by plays
        results.sort(key=lambda x: x['plays'], reverse=True)
        return results


def get_win_records(disp_name=None):
    if disp_name is not None:
        return db.search((where('type') == 'win_record') & (where('disp_name') == disp_name))
    else:
        return db.search(where('type') == 'win_record')


def get_stocks(user_id):
    return db.search((where('type') == 'stock') &
                     (where('user_id') == user_id))


def get_stocks_by_disp(disp_name):
    return db.search((where('type') == 'stock') &
                     (where('disp_name') == disp_name))


def get_tip_records(disp_name=None):
    if disp_name is not None:
        return db.search((where('type') == 'usertips') & (where('name') == disp_name))
    else:
        return db.search(where('type') == 'usertips')
        
     
def get_export():
    result = db.all()
    return result
    
    
def get_win_records_by_clip(clip_name):
    return db.search((where('type') == 'win_record') & (where('clip') == clip_name))
    
    
def get_stock_by_clip(clip_name):
    return db.search((where('type') == 'stock') & (where('clip') == clip_name))