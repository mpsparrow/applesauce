import discord
from discord.ext import commands
from utils.checks import is_guild_enabled
import random

class EightBall(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.responses = ["Certainly", "Definitely", "Yes", "Maybe", "No", "Absolutely not", "I don't think so"]

    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.command(name="8ball", description="Predicts your future", usage="<question>")
    @is_guild_enabled()
    async def eightball(self, ctx):
        await ctx.send(random.choice(self.responses))
