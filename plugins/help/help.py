import discord
from discord.ext import commands

class AdvancedHelp(commands.Cog):
    """
    Custom commands
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="helping", description="Pings the bot")
    async def helping(self, ctx):
        """
        Pings the bot
        """
        await ctx.send('help!')