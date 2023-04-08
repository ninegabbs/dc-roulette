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

LIST_COMMANDS = ("`/roulette` - Brings up the starting menu\n"
    "`/my_coins` - Shows your coin balance\n"
    "`/my_bets` - Shows your active bets\n"
    "`/bet color (value) (bet_amount)` - Use this to bet on a color. You can choose red or black."
    " After you pick the color, input your bet amount as well!\n"
    "`/bet number (value) (bet_amount)` - Use this to bet on a number. You can choose any integer"
    " from 0 to 36. Number bets have a lower chance to win, but the winnings are spicy!"
    " After you pick the number, input your bet amount as well!")

SEPARATOR = "-------------------------------"
LOUD_SEPARATOR = f":bell:{SEPARATOR}:bell:"
ROUND_SEPARATOR = f":game_die:{SEPARATOR}:game_die:"
INTRO_SEPARATOR = f":palm_tree:{SEPARATOR}:palm_tree:"
