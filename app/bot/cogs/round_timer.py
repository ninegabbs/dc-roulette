from discord.ext import tasks, commands
from loguru import logger

from app.bot.constants.strings import LOUD_SEPARATOR, ROUND_SEPARATOR, INTRO_SEPARATOR
from app.bot.game import roulette_roll
import app.bot.service as service
from app.config import GAME_NAME, ROUND_DURATION_S

round_duration = int(ROUND_DURATION_S)

class RoundTimer(commands.Cog):
    __instance = None

    @classmethod
    def delete_instance(cls):
        cls.__instance = None

    def __init__(self, ctx):
        cls = self.__class__
        if cls.__instance is None:
            self.index = round_duration
            self.warning_time_s = 10
            self.__ctx = ctx
            self.timer.start()
            cls.__instance = self

    @tasks.loop(seconds=1.0, count=round_duration)
    async def timer(self):
        self.index -= 1
        if self.index == self.warning_time_s:
            await self.__ctx.send(f"{LOUD_SEPARATOR}\nOnly {self.warning_time_s} seconds left in " +
                f"this round of {GAME_NAME}.\nPlace your bets while you can!\n{LOUD_SEPARATOR}")

    @timer.before_loop
    async def before(self):
        logger.debug("Round is starting")
        self.active = True
        await self.__ctx.send(f"{ROUND_SEPARATOR}\nA round of {GAME_NAME} is starting!\n" +
            f"You can place multiple bets during the next {round_duration} seconds.\n{ROUND_SEPARATOR}")

    @timer.after_loop
    async def after(self):
        logger.debug("Round is finished")
        res = roulette_roll()
        winnings = service.determine_winners(res)
        if len(winnings):
            announcement = "Congratulations to all the winners:\n" +\
                "\n".join([f"<@{user}>: {data['won']} :coin:" for user, data in winnings.items()])
        else:
            announcement = "Unfortunately, this time there were no winners.\n" +\
                "(Except that I get to keep all your coins, mwahahaha)"
        await self.__ctx.send(f"{GAME_NAME} rolled\n{INTRO_SEPARATOR}\n" + " " * 10 +
                              f":{res['color']}_circle:**{res['color']} {res['number']}**\n" +
                              f"{INTRO_SEPARATOR}\n" + announcement)
        self.__class__.delete_instance()
