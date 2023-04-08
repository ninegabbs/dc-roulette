from discord.ext import tasks, commands
from loguru import logger

from app.bot.game import roulette_roll
import app.bot.service as service
from app.common.decorators import singleton
from app.config import GAME_NAME, ROUND_DURATION_S

round_duration = int(ROUND_DURATION_S)

@singleton
class RoundTimer(commands.Cog):
    def __init__(self, ctx):
        self.index = 0
        self.warning_time_s = 90
        self.__ctx = ctx
        self.timer.start()

    def reset(self):
        self.active = False
        self.index = 0

    def cog_unload(self):
        self.timer.cancel()

    @tasks.loop(seconds=1.0, count=round_duration)
    async def timer(self):
        self.index += 1
        logger.debug(f"index:{self.index}")
        if self.index == self.warning_time_s:
            await self.__ctx.send(f"Only 30 seconds left in this round of {GAME_NAME}.\n"
                                  "Place your bets while you can!")

    @timer.before_loop
    async def before(self):
        logger.debug("Round is starting")
        self.active = True
        await self.__ctx.send(f"A round of {GAME_NAME} is starting!\n"
                              "You can place multiple bets during the next 2 minutes.")

    @timer.after_loop
    async def after(self):
        logger.debug("Round is finished")
        res = roulette_roll()
        logger.debug(f"res>>>{res}")
        winnings = service.determine_winners(res)
        await self.__ctx.send(f"{GAME_NAME} rolled {res['color']}:{res['number']}!\n"
                              "Congratulations to all the winners:\n"
                              "\n".join([f"<@{user}>: {coins} coins" for user, coins in winnings.items()]))
        logger.debug("Sending message and destroying myself")
        del self
