from loguru import logger

from collections import defaultdict

from app.common.exceptions import ErrorInsufficientBalance, ErrorUserNotRegistered
from app.data.db import SQLiteClient

db = SQLiteClient()


def add_user(user):
    # if user exists but just doesn't have money, add 100
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
    if user_coins is None:
        raise ErrorUserNotRegistered("User must register before placing a bet")
    new_balance = user_coins - bet_amount
    if new_balance < 0:
        raise ErrorInsufficientBalance(f"User {user.display_name} has only {user_coins} coins, trying to place a bet of {bet_amount}.\n"
                                  "Adjust the amount and try again.")
    data = {
        "user_id": user.id,
        "amount": bet_amount,
        "number": selection if color_or_number == "number" else None,
        "color": selection if color_or_number == "color" else "",
    }
    db.add_bet(data)
    db.update_user_coins(user.id, new_balance)
    return new_balance

def fetch_active_bets_by_user(user):
    return db.fetch_active_bets_by_user(user.id)[0]

def determine_winners(roll_result):
    bets = db.fetch_active_bets_all()[0]

    # Mapping bets by user_id
    bets_by_user = defaultdict(list)
    for bet in bets:
        bets_by_user[bet[0]].append({
            "amount": bet[1],
            "number": bet[2],
            "color": bet[3]
        })
    users = db.fetch_users_by_id(list(bets_by_user.keys()))[0]
    # Preparing a dict which will hold user balances and winnings
    winnings = {}
    for user in users:
        winnings[user[0]] = {"balance": user[1], "won": 0}

    # Checking winning bets and updating user balances
    for user_id, data in bets_by_user.items():
        user = winnings[user_id]
        won = 0
        for d in data:
            if d["number"] and d["number"] == roll_result["number"]:
                won += d["amount"] * 36
            elif d["color"] == roll_result["color"]:
                won = d["amount"] * 2
        user["balance"] += won
        user["won"] += won

    # Filtering out losers
    winnings = dict(filter(lambda kv: kv[1]['won'] > 0, winnings.items()))
    # Updating user balances in DB
    to_update = [{"user_id": id, "balance": data["balance"]} for id,data in winnings.items()]
    db.update_user_coins_batch(to_update)

    db.update_bets_deactivate_all()
    return winnings
