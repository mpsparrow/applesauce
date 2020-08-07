import discord
from discord.ext import commands

class Manage2(commands.Cog):
    """
    Management commands
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ping2", description="Pings the bot")
    async def ping2(self, ctx):
        """
        Pings the bot
        """
        await ctx.send('pong2!')