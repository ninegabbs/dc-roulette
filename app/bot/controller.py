import discord
from discord.ext import tasks, commands

from loguru import logger

from app.bot.cogs.round_timer import RoundTimer
import app.bot.constants.commands as cmd
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
            error = service.add_user(user)
            if error and type(error).__name__ == "IntegrityError":
                await interaction.response.send_message(
                    f"User <@{user_id}> is already registered as a player.\n"
                    "Try `/bet (color)` or `/bet (number)` in order to place a bet."   
                )
            elif error:
                await interaction.response.send_message(
                    f"{type(error).__name__} occured while trying to register '{user.display_name}'\n"
                    "Please try again later or contact support"
                )
            else:
                await interaction.response.send_message(
                    "Welcome to the fold!\n"
                    "You've been awarded 100 coins.\n"
                    "Try `/bet (color)` or `/bet (number)` in order to place a bet."
                )
        elif select.values[0] == cmd.RULES:
            await interaction.response.send_message(RESP_RULES)
        elif select.values[0] == cmd.COINS:
            coins, error = service.get_coins(user)
            if error:
                await interaction.response.send_message(
                    f"{type(error).__name__} occured while trying to fetch balance of '{user.display_name}'\n"
                    "Please try again later or contact support"
                )
            elif coins is None:
                await interaction.response.send_message(
                    f"User <@{user_id}> is not registered"
                )
            else:
                await interaction.response.send_message(
                    f"User <@{user_id}> has a balance of {coins} coins"
                )

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
    RoundTimer(ctx)

@bot.command(guild_ids=["1093221126504710305"])
async def my_bets(ctx: discord.ApplicationContext):
    bets = service.fetch_active_bets_by_user(ctx.user)
    if len(bets) > 0:
        await ctx.respond(
            f"<@{ctx.user.id}>, your bets are:\n" +
            "\n".join([f"{bet[1]} coins on {bet[2] if bet[2] else bet[3]}" for bet in bets])
        )
    else:
        await ctx.respond(f"@{ctx.user.id}, you have no active bets")
