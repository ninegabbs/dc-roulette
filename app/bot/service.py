from sqlite3 import IntegrityError

from app.common.exceptions import InsufficientBalance
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

def add_bet(user, color_or_number, selection, bet_amount):
    user_coins, error = fetch_coins(user)
    if error:
        return error
    if user_coins < bet_amount:
        raise InsufficientBalance(f"User {user.display_name} has only {user_coins} coins, trying to place a bet of {bet_amount}.\n"
                                  "Adjust the amount and try again.")
    data = {
        "user_id": user.id,
        "amount": bet_amount,
        "number": selection if color_or_number == "number" else 0,
        "color": selection if color_or_number == "color" else "",
    }
    return db.add_bet(data)

def fetch_active_bets_by_user(user):
    return db.fetch_active_bets_by_user(user.id)