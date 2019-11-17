import discord
from discord.ext import commands
from cogs.utils import checks

class Reactions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot



def setup(bot):
    bot.add_cog(Reactions(bot))
