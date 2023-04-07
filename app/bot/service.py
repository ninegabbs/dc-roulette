from sqlite3 import IntegrityError

from app.data.db import SQLiteClient

db = SQLiteClient()


def add_user(user):
    return db.add_user(user.id)

def fetch_coins(user):
    res, error = fetch_user_by_id(user)
    if res and len(res) > 1:
        return res[1], error
    return res, error

def fetch_user_by_id(user):
    return db.fetch_user_by_id(user.id)
