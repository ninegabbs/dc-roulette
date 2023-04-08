import discord
from discord.ext import tasks, commands

from loguru import logger

from app.bot.cogs.round_timer import RoundTimer
import app.bot.constants.commands as cmd
from app.bot.constants.strings import RESP_RULES
import app.bot.service as service
from app.common.exceptions import UserError
from app.config import TOKEN

global bot
bot = discord.Bot()

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
                value=cmd.REGISTER
            ),
            discord.SelectOption(
                label="Read rules",
                description="Lists the game rules",
                value=cmd.RULES
            ),
            discord.SelectOption(
                label="Check coin balance",
                description="Displays your current coin balance",
                value=cmd.COINS
            )
        ]
    )
    async def select_callback(self, select, interaction : discord.interactions.Interaction):
        user = interaction.user
        user_id = user.id
        if select.values[0] == cmd.REGISTER:
            try:
                service.add_user(user)
                await interaction.response.send_message(
                    f"Welcome to the fold, <@{user_id}>!\nYou've been awarded 100 coins.\n"
                    "Try `/bet` command in order to place a bet.")
            except UserError as ue:
                logger.warning(ue)
                await interaction.response.send_message(ue)
        elif select.values[0] == cmd.RULES:
            await interaction.response.send_message(RESP_RULES)
        elif select.values[0] == cmd.COINS:
            try:
                coins = service.get_coins(user)
                await interaction.response.send_message(
                    f"User <@{user_id}> has a balance of {coins} coins"
                )
            except UserError as ue:
                logger.warning(ue)
                await interaction.response.send_message(ue)

@bot.command()
async def roulette(ctx: discord.ApplicationContext):
    await ctx.respond("Welcome! What would you like to do?")
    await ctx.send(view=MenuView())

async def determine_bet_selection(ctx: discord.AutocompleteContext):
    color_or_number = ctx.options['color_or_number']
    if color_or_number == "color":
        return ["red", "black"]
    else:
        return [str(i) for i in range(0,37)]

@bot.command()
async def bet(
    ctx : discord.ApplicationContext,
    color_or_number: discord.Option(
        str,
        choices=["color", "number"],
        description="Choose whether you're betting on color or number"
    ),
    selection : discord.Option(
        str,
        autocomplete=discord.utils.basic_autocomplete(determine_bet_selection),
        description="Select an appropriate color or number value to bet on"
    ),
    bet_amount: discord.Option(int, description="Input the amount of coins you're betting")
):
    try:
        service.add_bet(ctx.user, color_or_number, selection, bet_amount)
        await ctx.respond(f"Bet accepted: {color_or_number}:{selection} for {bet_amount} coins")
        RoundTimer(ctx)
    except UserError as ue:
        logger.error(ue)
        await ctx.respond(ue)

@bot.command()
async def my_bets(ctx: discord.ApplicationContext):
    bets = service.fetch_active_bets_by_user(ctx.user)
    if len(bets) > 0:
        await ctx.respond(
            f"<@{ctx.user.id}>, your bets are:\n" +
            "\n".join([f"{bet[1]} coins on {bet[2] if bet[2] else bet[3]}" for bet in bets])
        )
    else:
        await ctx.respond(f"<@{ctx.user.id}>, you have no active bets")
