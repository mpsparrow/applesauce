import discord
from discord.ext import commands

class Debugger(commands.Cog):
    """
    Debugging tools
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ping", description="Pings the bot and returns latency")
    @commands.is_owner()
    async def ping(self, ctx):
        """
        Pings the bot and returns latency
        """
        await ctx.send(f"pong! {self.bot.latency}")