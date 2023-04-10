from discord.ext import tasks, commands
from loguru import logger

from app.bot.constants.strings import (TIMER_RUNNING_OUT_MSG,
                                       TIMER_START_MSG,
                                       TIMER_WINNERS_MSG,
                                       TIMER_NO_WINNERS,
                                       TIMER_ROLLED_MSG,
                                       ROUND_SEPARATOR)
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
            await self.__ctx.send(TIMER_RUNNING_OUT_MSG.format(warning_time_s=self.warning_time_s))

    @timer.before_loop
    async def before(self):
        logger.debug("Round is starting")
        self.active = True
        await self.__ctx.send(TIMER_START_MSG.format(round_duration=round_duration))

    @timer.after_loop
    async def after(self):
        logger.debug("Round is finished")
        res = roulette_roll()
        winnings = service.determine_winners(res)
        if len(winnings):
            announcement = TIMER_WINNERS_MSG +\
                "\n".join([f"<@{user}>: {data['won']} :coin:" for user, data in winnings.items()])
        else:
            announcement = TIMER_NO_WINNERS
        await self.__ctx.send(TIMER_ROLLED_MSG.format(color=res['color'], number=res['number']) +\
            announcement)
        self.__class__.delete_instance()
