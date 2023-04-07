import discord

from loguru import logger

import app.bot.constants.commands as commands
from app.bot.constants.strings import RESP_RULES
import app.bot.service as service
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

@bot.command()
async def roulette(ctx):
    await ctx.send("Welcome! What would you like to do?", view=MenuView())
    await ctx.respond("-----")
