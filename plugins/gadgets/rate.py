import discord
from discord.ext import commands
from utils.checks import is_guild_enabled
import random

class Rate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="rate", description="Rates between 1 and 10")
    @is_guild_enabled()
    async def rate(self, ctx):
        await ctx.send(f"{random.randint(1, 10)}/10")