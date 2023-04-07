from app.bot.constants.game_values import RED_NUMBERS_STR, BLACK_NUMBERS_STR


RESP_RULES = ("The game rules are as follows:\n"
    "Players can place bets on a specific number (0-36) or color (red or black).\n"
    f"Red roulette numbers are: {RED_NUMBERS_STR}\n"
    f"Black roulette numbers are: {BLACK_NUMBERS_STR}\n"
    "0 is green.\n"
    "- A spin happens everytime a player places a bet.\n"
    "- Each roulette spin has a random outcome, determining the winning number and color.\n"
    "- For correctly guessed color winnings are 2 times the bet sum\n"
    "- For correctly guessed number, winnings are 36 times the bet sum"
    "- If you run out coins, you can `!enter` once again")
