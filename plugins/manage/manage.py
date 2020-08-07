import discord
import pymongo
import importlib
from discord.ext import commands
from discord.ext.commands import has_permissions
from utils.database.actions import connect
from utils.logger import pluginLog

class Manage(commands.Cog):
    """
    Management commands
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="plugin", description="Plugin management", usage="plugin <action> <plugin name>", aliases=["plugin"])
    @commands.has_permissions(manage_guild=True)
    async def plugin(self, ctx):
        """
        Command group for plugin management.
        :param ctx:
        """

    @plugin.command(name="load", description="Load a plugin", usage="plugin load <plugin name>", aliases=["l"])
    @commands.is_owner()
    async def load(self, ctx, plugin):
        """
        Load a plugin
        `load_extension <https://discordpy.readthedocs.io/en/latest/ext/commands/api.html?highlight=load_extension#discord.ext.commands.Bot.load_extension>`
        :param ctx:
        :param str name: Plugin name
        """
        try:
            self.bot.load_extension(f"plugins.{plugin}")
            i = importlib.import_module(f"plugins.{plugin}")
            pluginINFO = { "_id": plugin, 
                            "plugin_name": i.PLUGIN_NAME,
                            "cog_names": i.COG_NAMES,
                            "version": i.VERSION,
                            "loaded": True }
            pluginCol.update_one({ "_id": plugin }, { "$set": pluginINFO }, upsert=True)
            pluginLog.info(f"Loaded: {plugin} ({i.PLUGIN_NAME}) | Cogs: {i.COG_NAMES} | Version: {i.VERSION}")
            await ctx.message.add_reaction("✅")
        except commands.ExtensionNotFound:
            # The plugin could not be found.
            pluginLog.error(f"plugins.{plugin}: not found (ExtensionNotFound)")
            await ctx.message.add_reaction("❌")
        except commands.ExtensionAlreadyLoaded:
            # The plugin was already loaded.
            pluginLog.info(f"plugins.{plugin}: already loaded (ExtensionAlreadyLoaded)")
            await ctx.message.add_reaction("✅")
        except commands.NoEntryPointError:
            # The plugin does not have a setup function.
            pluginLog.error(f"plugins.{plugin}: no setup function (NoEntryPointError)")
            await ctx.message.add_reaction("⚠️")
        except commands.ExtensionFailed:
            # The plugin setup function has an execution error.
            pluginLog.error(f"plugins.{plugin}: execution error (ExtensionFailed)")
            await ctx.message.add_reaction("⚠️")
        except Exception as error:
            self.bot.unload_extension(f"plugins.{plugin}")
            pluginLog.error(f"plugins.{plugin}: variables not properly defined. Plugin unloaded.")
            await ctx.message.add_reaction("⚠️")

    @plugin.command(name="unload", description="Unload a plugin", usage="plugin unload <plugin name>", aliases=["u"])
    @commands.is_owner()
    async def unload(self, ctx, plugin):
        """
        Unload a plugin
        `unload_extension <https://discordpy.readthedocs.io/en/latest/ext/commands/api.html?highlight=unload_extension#discord.ext.commands.Bot.unload_extension>`
        :param ctx:
        :param str plugin: Plugin name
        """
        try:
            self.bot.unload_extension(f"plugins.{plugin}")
            i = importlib.import_module(f"plugins.{plugin}")
            pluginINFO = { "_id": plugin, 
                            "plugin_name": i.PLUGIN_NAME,
                            "cog_names": i.COG_NAMES,
                            "version": i.VERSION,
                            "loaded": False }
            pluginCol.update_one({ "_id": plugin }, { "$set": pluginINFO }, upsert=True)
            pluginLog.info(f"Unloaded: {plugin} ({i.PLUGIN_NAME}) | Cogs: {i.COG_NAMES} | Version: {i.VERSION}")
            await ctx.message.add_reaction("✅")
        except commands.ExtensionNotLoaded:
            # The plugin was not found or unloaded.
            pluginLog.error(f"plugins.{plugin}: unable to be found and unloaded. (ExtensionNotLoaded)")
            await ctx.message.add_reaction("❌")
        except Exception as error:
            pluginLog.error(f"plugins.{plugin}: unknown unloading plugin error.")
            await ctx.message.add_reaction("⚠️")