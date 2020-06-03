import discord
from discord.ext import commands
import random
import time

class Hank(commands.Cog):
    """
    Hanks when you hank.
    """
    def __init__(self, bot):
        self.bot = bot
        self.hankTimer = 0
        self.randomVal = 0

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if (int(message.channel.id) == 459824576688291840):
            if (("<:hank:461015208224358440>" in message.content) and ((time.time() - self.hankTimer) > self.randomVal)):
                self.hankTimer = time.time()
                self.randomVal = random.randint(240, 900)
                channel = self.bot.get_channel(459824576688291840)
                await channel.send("<:hank:461015208224358440>")
                return

def setup(bot):
    bot.add_cog(Hank(bot))