from app.bot.constants.game_values import RED_NUMBERS_STR, BLACK_NUMBERS_STR
from app.config import GAME_NAME

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

REGISTER_SUCCESS_MSG = "Welcome to the fold, <@{user_id}>!\nYou've been awarded 100 coins.\n" +\
    "Try `/bet` command in order to place a bet."

REGISTER_FAIL_MSG = "<@{user_id}> is already registered!\nTry `/bet` commands in order to place a bet."

INTRO_MSG = f"{INTRO_SEPARATOR}\nWelcome to `{GAME_NAME}`! What would you like to do?\n{INTRO_SEPARATOR}"

BET_SUCCESS_MSG = SEPARATOR + "Bet accepted: :{value}_circle:**{value}** for {bet_amount} :coin:" +\
    SEPARATOR

MY_BETS_SUCCESS_MSG = "<@{user_id}>, your bets are:\n{bets}"

MY_BETS_FAIL_MSG = "<@{user_id}>, you have no active bets"

MY_COINS_SUCCESS_MSG = "User <@{user_id}> has a balance of {coins} :coin:"

USER_NOT_REGISTERED_MSG = "User <@{user_id}> is not registered"

BET_FAIL_NO_USER_MSG = "User must register before placing a bet"

BET_FAIL_INVALID_NUMBER_MSG = "<@{user_id}>, you can only bet on numbers between 0 and 36!"

BET_FAIL_INVALID_COLOR_MSG = "<@{user_id}>, you can only bet on colors red and black!"

BET_FAIL_INVALID_AMOUNT_MSG = "<@{user.id}>, invalid bet amount!"

BET_FAIL_0_BALANCE_MSG = "<@{user_id}>, you've run out of coins!\n" +\
    "You can register again to get a new batch of 100."

BET_FAIL_INSUFFICIENT_BALANCE_MSG = "User <@{user_id}> has only {user_coins} coins, while " +\
    "trying to place a bet of {bet_amount}.\nAdjust the amount and try again."

BET_FAIL_NOT_REGISTERED_MSG = "User must register before placing a bet"

TIMER_RUNNING_OUT_MSG = f"{LOUD_SEPARATOR}\nOnly" + "{warning_time_s} seconds left in " +\
                f"this round of {GAME_NAME}.\nPlace your bets while you can!\n{LOUD_SEPARATOR}"

TIMER_START_MSG = f"{ROUND_SEPARATOR}\nA round of {GAME_NAME} is starting!\n" +\
            "You can place multiple bets during the next {round_duration} seconds.\n" + ROUND_SEPARATOR

TIMER_WINNERS_MSG = "Congratulations to all the winners:\n"

TIMER_NO_WINNERS = "Unfortunately, this time there were no winners.\n" +\
    "(Except that I get to keep all your coins, mwahahaha)"

TIMER_ROLLED_MSG = f"{GAME_NAME} rolled\n{INTRO_SEPARATOR}\n" + " " * 10 +\
    ":{color}_circle:**{color} {number}**\n" + f"{INTRO_SEPARATOR}\n"
