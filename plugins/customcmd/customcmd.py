import discord
from discord.ext import commands

class CustomCMD(commands.Cog):
    """
    Custom commands
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="custom", description="Pings the bot")
    async def custom(self, ctx):
        """
        Pings the bot
        """
        await ctx.send('custom!')