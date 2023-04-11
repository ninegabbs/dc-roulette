from loguru import logger

from collections import defaultdict

from app.bot.constants.strings import (REGISTER_FAIL_MSG,
                                       USER_NOT_REGISTERED_MSG,
                                       BET_FAIL_INVALID_NUMBER_MSG,
                                       BET_FAIL_INVALID_COLOR_MSG,
                                       BET_FAIL_INVALID_AMOUNT_MSG,
                                       BET_FAIL_0_BALANCE_MSG,
                                       BET_FAIL_INSUFFICIENT_BALANCE_MSG,
                                       BET_FAIL_NOT_REGISTERED_MSG)
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
        raise UserError(REGISTER_FAIL_MSG.format(user_id=user_id))

def get_coins(user):
    user_id = user.id
    res = db.fetch_user_by_id(user_id)
    if res is None:
        raise UserError(USER_NOT_REGISTERED_MSG.format(user_id=user_id))
    return res[1]

def add_bet(user, bet_value, bet_amount):
    user_coins = get_coins(user)
    user_id = user.id
    
    if bet_value.isnumeric():
        bet_num = int(bet_value)
        bet_clr = None
    else:
        bet_num = None
        bet_clr = bet_value

    if bet_num and bet_num not in range(0, 37):
        raise UserError(BET_FAIL_INVALID_NUMBER_MSG.format(user_id=user_id))

    if bet_clr and bet_clr not in ["red", "black"]:
        raise UserError(BET_FAIL_INVALID_COLOR_MSG.format(user_id=user_id))

    if bet_amount < 1:
        raise UserError(BET_FAIL_INVALID_AMOUNT_MSG.format(user_id=user_id))

    if user_coins == 0:
        raise UserError(BET_FAIL_0_BALANCE_MSG.format(user_id=user_id))

    new_balance = user_coins - bet_amount
    if new_balance < 0:
        raise UserError(BET_FAIL_INSUFFICIENT_BALANCE_MSG.format(user_id=user_id,
                                                                 user_coins=user_coins,
                                                                 bet_amount=bet_amount))
    data = {
        "user_id": user_id,
        "amount": bet_amount,
        "number": bet_num,
        "color": bet_clr,
    }
    db.add_bet(data)
    db.update_user_coins(user_id, new_balance)
    return new_balance

def fetch_active_bets_by_user(user):
    return db.fetch_active_bets_by_user(user.id)

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
