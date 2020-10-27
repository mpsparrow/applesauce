import discord
from discord.ext import commands
from utils.checks import is_guild_enabled
import random

class Chance(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.command(name="chance", description="Tells you your chances of success")
    @is_guild_enabled()
    async def chance(self, ctx):
        await ctx.send(f"{random.randint(0, 100)}%")