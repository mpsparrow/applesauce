import discord
from discord.ext import commands
from utils.checks import is_guild_enabled
import random

coin_emotes = {
    0: "🌑",
    1: "🌕"
}

class Coinflip(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="coinflip", description="Flips a coin", aliases=["coin", "flip"])
    @is_guild_enabled()
    async def coinflip(self, ctx):
        await ctx.message.add_reaction(coin_emotes[random.randint(0, 1)])