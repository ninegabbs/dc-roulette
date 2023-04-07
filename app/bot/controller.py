import discord

from loguru import logger

import app.bot.constants.commands as commands
from app.bot.constants.strings import RESP_RULES
from app.bot.game import Game
import app.bot.service as service
from app.config import TOKEN

global bot
bot = discord.Bot()
game = Game()

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
                value=commands.REGISTER
            ),
            discord.SelectOption(
                label="Read rules",
                description="Lists the game rules",
                value=commands.RULES
            ),
            discord.SelectOption(
                label="Check coin balance",
                description="Displays your current coin balance",
                value=commands.COINS
            ),
            discord.SelectOption(
                label="Place a bet",
                description="Brings up a dialog to place bets",
                value=commands.BET
            )
        ]
    )
    async def select_callback(self, select, interaction : discord.interactions.Interaction):
        user = interaction.user
        display_name = user.display_name
        if select.values[0] == commands.REGISTER:
            error = service.add_user(user)
            if error and type(error).__name__ == "IntegrityError":
                await interaction.response.send_message(
                    f"User '@{display_name}' is already registered as a player.\n"
                    "Try `/bet (color)` or `/bet (number)` in order to place a bet."   
                )
            elif error:
                await interaction.response.send_message(
                    f"{type(error).__name__} occured while trying to register '{display_name}'\n"
                    "Please try again later or contact support"
                )
            else:
                await interaction.response.send_message(
                    "Welcome to the fold!\n"
                    "You've been awarded 100 coins.\n"
                    "Try `/bet (color)` or `/bet (number)` in order to place a bet."
                )
        elif select.values[0] == commands.RULES:
            await interaction.response.send_message(RESP_RULES)
        elif select.values[0] == commands.COINS:
            coins, error = service.fetch_coins(user)
            if error:
                await interaction.response.send_message(
                    f"{type(error).__name__} occured while trying to fetch balance of '{display_name}'\n"
                    "Please try again later or contact support"
                )
            elif coins is None:
                await interaction.response.send_message(
                    f"User '@{display_name}' is not registered"
                )
            else:
                await interaction.response.send_message(
                    f"User '@{display_name}' has a balance of {coins} coins"
                )
        elif select.values[0] == commands.BET:
            interaction.response.send_message("Try `/bet (color)` or `/bet (number)` in order to place a bet.")

@bot.command()
async def roulette(ctx: discord.ApplicationContext):
    await ctx.send("Welcome! What would you like to do?", view=MenuView())
    await ctx.respond("-----")


async def determine_selection(ctx: discord.AutocompleteContext):
    color_or_number = ctx.options['color_or_number']
    if color_or_number == "color":
        return ["red", "black"]
    else:
        return [str(i) for i in range(0,37)]

@bot.command()
async def bet(
    ctx : discord.ApplicationContext,
    color_or_number: discord.Option(str, choices=["color", "number"], description="Choose whether you're betting on color or number"),
    selection : discord.Option(str, autocomplete=discord.utils.basic_autocomplete(determine_selection), description="Select an appropriate color or number value to bet on"),
    bet_amount: discord.Option(int, description="Input the amount of coins you're betting")
):
    service.add_bet(ctx.user, color_or_number, selection, bet_amount)
    await ctx.respond(f"Bet accepted: {color_or_number}:{selection} for {bet_amount} coins")
    # if no errors
    if not game.is_pot_active:
        game.is_pot_active += True
    game.total_pot += bet_amount

@bot.command()
async def my_bets(ctx: discord.ApplicationContext):
    bets = service.fetch_active_bets_by_user(ctx.user)
    if len(bets) > 0:
        await ctx.respond(f"@{ctx.user.display_name}, your bets are:\n"
                        f"{bet[1]} coins on {bet[2] if bet[2] else bet[3]}\n" for bet in bets)
    else:
        await ctx.respond(f"@{ctx.user.display_name}, you have no active bets")
