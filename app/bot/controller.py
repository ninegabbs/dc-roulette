import discord

from loguru import logger

from app.bot.cogs.round_timer import RoundTimer
import app.bot.constants.choices as choices
from app.bot.constants.strings import (RESP_RULES,
                                       LIST_COMMANDS,
                                       REGISTER_SUCCESS_MSG,
                                       INTRO_MSG,
                                       BET_SUCCESS_COLOR_MSG,
                                       BET_SUCCESS_NUMBER_MSG,
                                       MY_BETS_SUCCESS_MSG,
                                       MY_BETS_FAIL_MSG,
                                       MY_COINS_SUCCESS_MSG)
import app.bot.service as service
from app.common.exceptions import UserError
from app.config import TOKEN, GAME_NAME

global bot
bot = discord.Bot()
bet = bot.create_group("bet", "Place a bet")

def launch_bot():
    logger.info("Bot is running!")
    bot.run(TOKEN)

class MenuView(discord.ui.View):
    @discord.ui.select(
        placeholder = "Choose an action",
        min_values = 1,
        max_values = 1,
        options = [
            discord.SelectOption(
                label="Register",
                description=f"Gives you 100 coins and adds you to the player ranks",
                value=choices.REGISTER
            ),
            discord.SelectOption(
                label="Read rules",
                description="Lists the game rules",
                value=choices.RULES
            ),
            discord.SelectOption(
                label="List commands",
                description=f"Lists all commands usable in {GAME_NAME}",
                value=choices.COMMANDS
            )
        ]
    )
    async def select_callback(self, select, interaction : discord.interactions.Interaction):
        user = interaction.user
        user_id = user.id
        if select.values[0] == choices.REGISTER:
            try:
                service.add_user(user)
                await interaction.response.send_message(REGISTER_SUCCESS_MSG.format(user_id=user_id))
            except UserError as ue:
                logger.error(ue)
                await interaction.response.send_message(str(ue))
        elif select.values[0] == choices.RULES:
            await interaction.response.send_message(RESP_RULES)
        elif select.values[0] == choices.COMMANDS:
            await interaction.response.send_message(LIST_COMMANDS)

@bot.command()
async def roulette(ctx: discord.ApplicationContext):
    await ctx.respond(INTRO_MSG)
    await ctx.send(view=MenuView())

@bet.command()
async def color(
    ctx : discord.ApplicationContext,
    value : discord.Option(
        str,
        choices=["red", "black"],
        description="Choose either red or black color to bet on"
    ),
    bet_amount: discord.Option(int, description="Input the amount of coins you're betting")
):
    try:
        service.add_bet(ctx.user, value, bet_amount)
        await ctx.respond(BET_SUCCESS_COLOR_MSG.format(value=value, bet_amount=bet_amount))
        RoundTimer(ctx)
    except UserError as ue:
        logger.error(ue)
        await ctx.respond(str(ue))

@bet.command()
async def number(
    ctx : discord.ApplicationContext,
    value : discord.Option(str, description="Type in a number between 0 and 36"),
    bet_amount: discord.Option(int, description="Input the amount of coins you're betting")
):
    try:
        service.add_bet(ctx.user, value, bet_amount)
        await ctx.respond(BET_SUCCESS_NUMBER_MSG.format(value=value, bet_amount=bet_amount))
        RoundTimer(ctx)
    except UserError as ue:
        logger.error(ue)
        await ctx.respond(str(ue))

@bot.command()
async def my_bets(ctx: discord.ApplicationContext):
    bets = service.fetch_active_bets_by_user(ctx.user)
    user_id = ctx.user.id
    if len(bets) > 0:
        # bet[1] - amount; bet[2] - number; bet[3] - color
        bets_list_str = [f"{bet[1]} coins on {bet[2] if bet[2] else bet[3]}" for bet in bets]
        await ctx.respond(MY_BETS_SUCCESS_MSG.format(user_id=user_id,
                                                     bets="\n".join(bets_list_str)))
    else:
        await ctx.respond(MY_BETS_FAIL_MSG.format(user_id=user_id))

@bot.command()
async def my_coins(ctx: discord.ApplicationContext):
    try:
        coins = service.get_coins(ctx.user)
        await ctx.respond(MY_COINS_SUCCESS_MSG.format(user_id=ctx.user.id, coins=coins))
    except UserError as ue:
        logger.error(ue)
        await ctx.respond(str(ue))
