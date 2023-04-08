from loguru import logger

from collections import defaultdict

from app.common.exceptions import UserError
from app.data.db import SQLiteClient

db = SQLiteClient()


def add_user(user):
    user_id = user.id
    user_data = db.fetch_user_by_id(user_id)
    if not user_data:
        return db.add_user(user.id)
    # If a user is out of coins, restarting their game
    if user_data[1] < 1:
        db.update_user_coins(user_id, 100)
    else:
        raise UserError(f"<@{user.id}> is already registered!\n"
                        "Try `/bet` command in order to place a bet.")

def get_coins(user):
    user_id = user.id
    res = db.fetch_user_by_id(user_id)
    if res is None:
        raise UserError(f"User <@{user_id}> is not registered")
    return res[1]

def add_bet(user, color_or_number, selection, bet_amount):
    user_coins = get_coins(user)
    if user_coins is None:
        raise UserError("User must register before placing a bet")
    elif user_coins == 0:
        raise UserError(f"<@{user.id}>, you've run out of coins!\n"
                                 "You can register again to get a new batch of 100.")
    new_balance = user_coins - bet_amount
    if new_balance < 0:
        raise UserError(f"User <@{user.id}> has only {user_coins} coins, while "
                                       f"trying to place a bet of {bet_amount}.\n"
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
    bets = db.fetch_active_bets_by_user(user.id)
    if bets is None:
        raise UserError("User must register before placing a bet")
    return bets

def determine_winners(roll_result):
    bets = db.fetch_active_bets_all()

    # Mapping bets by user_id
    bets_by_user = defaultdict(list)
    for bet in bets:
        bets_by_user[bet[0]].append({
            "amount": bet[1],
            "number": bet[2],
            "color": bet[3]
        })
    users = db.fetch_users_by_id(list(bets_by_user.keys()))
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
