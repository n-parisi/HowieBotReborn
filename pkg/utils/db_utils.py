from tinydb import TinyDB, where
from tinydb.operations import subtract, set, decrement, add
import uuid

db = TinyDB('resources/db.json')


def check_wagers(clip, total_clip_count):
    is_wager = where('type') == 'wager'
    # decrease count of miss
    db.update(decrement('count'),
              is_wager and where('clip') != 'clip')
    # delete the zeros
    db.remove(is_wager and where('count') == 0)
    # get the hits
    results = db.search(is_wager and where('clip') == clip)
    winners = []
    for result in results:
        # pay out
        pay_out = result['amount'] * total_clip_count / result['start_count']
        db.update(add('bucks', pay_out),
                  where('type') == 'account' and where('id') == result['user_id'])
        # delete wager record
        db.remove(is_wager and where('wager_id') == result['wager_id'])
        winners.append((result['disp_name'], pay_out, result['clip']))

    print(winners)
    return winners


def new_account(discord_id, name):
    db.insert({'type': 'account',
               'id': discord_id,
               'name': name,
               'bucks': 100})
    return get_account(discord_id)


def new_wager(disp_name, account, amount, clip, count):
    # deduct amount
    db.update(subtract('bucks', amount),
              where('type') == 'account' and where('id') == account['id'])
    # update display name if needed
    db.update(set('name', disp_name),
              where('type') == 'account' and where('id') == account['id'])
    # place wager
    db.insert({'type': 'wager',
               'wager_id': str(uuid.uuid4()),
               'user_id': account['id'],
               'disp_name' : disp_name,
               'clip': clip,
               'amount': amount,
               'count': count,
               'start_count': count})


def new_macro(macro_name, macro):
    db.insert({'type': 'macro',
               'name': macro_name,
               'macro': macro})


def get_macro(macro_name):
    result = db.search(where('type') == 'macro' and where('name') == macro_name)
    return result[0] if len(result) > 0 else None


def get_accounts():
    return db.search(where('type') == 'account')


def get_account(discord_id):
    result = db.search(where('type') == 'account' and where('id') == discord_id)
    return result[0] if len(result) > 0 else None


def get_wagers():
    return db.search(where('type') == 'wager')
