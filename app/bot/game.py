import random

from app.bot.constants.game_values import RED_NUMBERS, BLACK_NUMBERS

def roulette_roll():
    res = random.randint(0, 37)
    color = "red" if res in RED_NUMBERS else "black" if res in BLACK_NUMBERS else "green"
    return {
        "number": res,
        "color": color
    }
