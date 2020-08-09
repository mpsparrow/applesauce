import discord
from discord.ext import commands
from utils.config import readTXT

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
        await ctx.send(f"pong! {round(self.bot.latency*1000, 1)}ms")

    @commands.command(name="startlog", description="Outputs startup.log")
    @commands.is_owner()
    async def startlog(self, ctx):
        try:
            await ctx.send(f"```{readTXT('logs/startup.log').read()}```")
        except configError:
            await ctx.message.add_reaction("❌")