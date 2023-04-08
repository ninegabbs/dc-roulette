import discord
from discord.ext import tasks, commands

from loguru import logger

from app.bot.cogs.round_timer import RoundTimer
import app.bot.constants.choices as choice
from app.bot.constants.strings import RESP_RULES, LIST_COMMANDS, SEPARATOR, INTRO_SEPARATOR
import app.bot.service as service
from app.common.exceptions import UserError
from app.config import TOKEN, GAME_NAME

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
                value=choice.REGISTER
            ),
            discord.SelectOption(
                label="Read rules",
                description="Lists the game rules",
                value=choice.RULES
            ),
            discord.SelectOption(
                label="List commands",
                description=f"Lists all commands usable in {GAME_NAME}",
                value=choice.COMMANDS
            )
        ]
    )
    async def select_callback(self, select, interaction : discord.interactions.Interaction):
        user = interaction.user
        user_id = user.id
        if select.values[0] == choice.REGISTER:
            try:
                service.add_user(user)
                await interaction.response.send_message(
                    f"Welcome to the fold, <@{user_id}>!\nYou've been awarded 100 coins.\n"
                    "Try `/bet` command in order to place a bet.")
            except UserError as ue:
                logger.warning(ue)
                await interaction.response.send_message(ue)
        elif select.values[0] == choice.RULES:
            await interaction.response.send_message(RESP_RULES)
        elif select.values[0] == choice.COMMANDS:
            await interaction.response.send_message(LIST_COMMANDS)

@bot.command(guild_ids=["1093221126504710305"])
async def roulette(ctx: discord.ApplicationContext):
    await ctx.respond(
        f"{INTRO_SEPARATOR}\nWelcome to `{GAME_NAME}`! What would you like to do?\n{INTRO_SEPARATOR}"
    )
    await ctx.send(view=MenuView())

async def determine_bet_selection(ctx: discord.AutocompleteContext):
    color_or_number = ctx.options['color_or_number']
    if color_or_number == "color":
        return ["red", "black"]
    else:
        return [str(i) for i in range(0,37)]

bet = bot.create_group("bet", "Place a bet")

@bet.command(guild_ids=["1093221126504710305"])
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
        await ctx.respond(f"Bet accepted: :{value}_circle:**{value}** for {bet_amount} :coin:")
        RoundTimer(ctx)
    except UserError as ue:
        logger.error(ue)
        await ctx.respond(ue)

@bet.command(guild_ids=["1093221126504710305"])
async def number(
    ctx : discord.ApplicationContext,
    value : discord.Option(str, description="Type in a number between 0 and 37"),
    bet_amount: discord.Option(int, description="Input the amount of coins you're betting")
):
    try:
        service.add_bet(ctx.user, value, bet_amount)
        await ctx.respond(f"{SEPARATOR}\nBet accepted: --**{value}**-- for {bet_amount} :coin:\n{SEPARATOR}")
        RoundTimer(ctx)
    except UserError as ue:
        logger.error(ue)
        await ctx.respond(ue)

@bot.command(guild_ids=["1093221126504710305"])
async def my_bets(ctx: discord.ApplicationContext):
    bets = service.fetch_active_bets_by_user(ctx.user)
    if len(bets) > 0:
        await ctx.respond(
            f"<@{ctx.user.id}>, your bets are:\n" +
            "\n".join([f"{bet[1]} coins on {bet[2] if bet[2] else bet[3]}" for bet in bets])
        )
    else:
        await ctx.respond(f"<@{ctx.user.id}>, you have no active bets")

@bot.command(guild_ids=["1093221126504710305"])
async def my_coins(ctx: discord.ApplicationContext):
    try:
        coins = service.get_coins(ctx.user)
        await ctx.respond(
            f"User <@{ctx.user.id}> has a balance of {coins} :coin:"
        )
    except UserError as ue:
        logger.warning(ue)
        await ctx.respond(ue)
