import discord
from discord.ext import commands
from utils.checks import is_guild_enabled

class CustomCMD(commands.Cog):
    """
    Custom commands
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="custom", description="Pings the bot")
    @is_guild_enabled()
    async def custom(self, ctx):
        """
        Pings the bot
        """
        await ctx.send('custom!')