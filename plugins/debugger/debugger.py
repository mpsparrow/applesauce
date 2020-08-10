import discord
import importlib
from discord.ext import commands
from utils.config import readTXT, readINI
from utils.database.actions import connect

class Debugger(commands.Cog):
    """
    Debugging tools
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="debug", description="Debugging", usage="<action>", aliases=["d", "debugging"], invoked_subcommand=True)
    @commands.is_owner()
    async def debug(self, ctx):
        """
        Command group for owner debugging
        :param ctx:
        """

    @debug.command(name="ping", description="Pings the bot and returns latency", aliases=["p"])
    @commands.is_owner()
    async def ping(self, ctx):
        """
        Pings the bot and returns latency
        """
        await ctx.send(f"pong! {round(self.bot.latency*1000, 1)}ms")

    @debug.command(name="startlog", description="Outputs startup.log", aliases=["log"])
    @commands.is_owner()
    async def startlog(self, ctx):
        """
        Outputs startup.log
        """
        await ctx.send(f"```{readTXT('logs/startup.log')}```")

    @debug.command(name="dbCleaner", description="Cleans database of invalid plugins", aliases=["cleaner", "clean"])
    @commands.is_owner()
    async def dbCleaner(self, ctx):
        """
        Cleans database of invalid plugins
        """
        pluginCol = connect()[readINI("config.ini")["MongoDB"]["database"]]["plugins"]
        folder = readINI("config.ini")["main"]["pluginFolder"]
        removed = 0
        total = 0

        # loops through all plugin documents in plugin collection
        for plugin in pluginCol.find():
            total += 1
            try:
                i = importlib.import_module(f"{folder}.{plugin['_id']}.plugininfo")
            except ModuleNotFoundError:
                pluginCol.delete_one({ "_id": plugin })
                removed += 1

        await ctx.send(f"Removed {removed}/{total}")