from tinydb import TinyDB, where

db = TinyDB('resources/db.json')


def new_account(discord_id, name):
    db.insert({'type': 'account',
               'id': discord_id,
               'name': name,
               'bucks': 100})


def new_macro(macro_name, macro):
    db.insert({'type': 'macro',
               'name': macro_name,
               'macro': macro})


def get_macro(macro_name):
    return db.search(where('type') == 'macro')[0]


def get_accounts():
    return db.search(where('type') == 'account')
