import discord
from discord.ext import commands

class Error(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        

def setup(bot):
    bot.add_cog(Error(bot))
