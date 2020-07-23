import discord
from discord.ext import commands

class Manage(commands.Cog):
    """
    Management commands
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ping", description="Pings the bot")
    async def ping(self, ctx):
        """
        Pings the bot
        """
        await ctx.send('pong!')