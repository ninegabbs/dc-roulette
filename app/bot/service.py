from sqlite3 import IntegrityError

from app.common.exceptions import InsufficientBalance
from app.data.db import SQLiteClient

db = SQLiteClient()


def add_user(user):
    return db.add_user(user.id)

def get_coins(user):
    res, error = fetch_user_by_id(user)
    if res and len(res) > 1:
        return res[1], error
    return res, error

def fetch_user_by_id(user):
    return db.fetch_user_by_id(user.id)

def add_bet(user, color_or_number, selection, bet_amount):
    user_coins, error = get_coins(user)
    # if error:
    #     return error
    new_balance = user_coins - bet_amount
    if new_balance < 0:
        raise InsufficientBalance(f"User {user.display_name} has only {user_coins} coins, trying to place a bet of {bet_amount}.\n"
                                  "Adjust the amount and try again.")
    data = {
        "user_id": user.id,
        "amount": bet_amount,
        "number": selection if color_or_number == "number" else 0,
        "color": selection if color_or_number == "color" else "",
    }
    db.add_bet(data)
    db.update_user_coins(user.id, new_balance)
    return new_balance

def fetch_active_bets_by_user(user):
    return db.fetch_active_bets_by_user(user.id)[0]

def determine_winners(roll_result):
    # bets = db.fetch_active_bets_all()
    # db.update_bets_deactivate_all()
    winnings = {"test_key": "test_value"}
    # map bets by user_id
    # fetch all users who played
    # loop over bets
    # check if it won -> update winnings and relevant user's balance
    # update user
    return winnings
