import os
import discord
import pymongo
import importlib
from discord.ext import commands
from discord.ext.commands import has_permissions
from utils.database.actions import connect
from utils.logger import pluginLog
from utils.config import readINI

class Manage(commands.Cog):
    """
    Plugin management commands
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="plugin", description="Plugin management", usage="<action>", aliases=["p", "plug"])
    @commands.has_permissions(manage_guild=True)
    async def plugin(self, ctx):
        """
        Command group for plugin management.
        :param ctx:
        """

    @plugin.command(name="all", description="List all loaded plugins", usage="<plugin name>", aliases=["a"])
    @commands.has_permissions(manage_guild=True)
    async def all(self, ctx, show_unloaded: bool=False):
        """
        List all loaded plugins
        :param ctx:
        :param show_unloaded: show unloaded plugins for owner
        """
        pluginCol = connect()["applesauce"]["plugins"] # connect to DB
        embed=discord.Embed(title='Plugins', color=0xc1c100)
        folder = readINI("config.ini")["main"]["pluginFolder"]

        if show_unloaded and await self.bot.is_owner(ctx.author):
            for plug in next(os.walk(folder))[1]:
                # skips '__pycache__' folder and any files
                if plug == "__pycache__":
                    continue

                try:
                    data = pluginCol.find_one({ "_id": plug })
                    loaded = "Loaded" if data['loaded'] else "Unloaded"
                    embed.add_field(name=f"{data['_id']} v{data['version']} ({loaded})", 
                                    value=data["description"], 
                                    inline=False)
                except TypeError:
                    # not in database
                    try:
                        # working
                        i = importlib.import_module(f"{folder}.{plug}")
                        embed.add_field(name=f"{plug} v{i.VERSION} (never loaded)", 
                                        value=i.DESCRIPTION, 
                                        inline=False)
                    except Exception as error:
                        # error in plugin
                        embed.add_field(name=f"{plug} (never loaded)(error)", 
                                        value="unknown", 
                                        inline=False)
        else:
            for x in pluginCol.find({ "loaded": True }):
                embed.add_field(name=x["_id"], 
                                value=x["description"], 
                                inline=False)
        await ctx.send(embed=embed)

    @plugin.command(name="load", description="Load a plugin", usage="<plugin name>", aliases=["l"])
    @commands.is_owner()
    async def load(self, ctx, plug):
        """
        Load a plugin
        `load_extension <https://discordpy.readthedocs.io/en/latest/ext/commands/api.html?highlight=load_extension#discord.ext.commands.Bot.load_extension>`
        :param ctx:
        :param str plug: Plugin name
        """
        try:
            folder = readINI("config.ini")["main"]["pluginFolder"]
            self.bot.load_extension(f"{folder}.{plug}")
            i = importlib.import_module(f"{folder}.{plug}")
            pluginCol = connect()["applesauce"]["plugins"] # connect to DB
            pluginINFO = { "_id": plug, 
                            "plugin_name": i.PLUGIN_NAME,
                            "cog_names": i.COG_NAMES,
                            "version": i.VERSION,
                            "author": i.AUTHOR,
                            "description": i.DESCRIPTION,
                            "load_on_start": i.LOAD_ON_START, 
                            "required": i.REQUIRED,
                            "loaded": True }
            pluginCol.update_one({ "_id": plug }, { "$set": pluginINFO }, upsert=True)
            pluginLog.info(f"Loaded: {plug} ({i.PLUGIN_NAME}) | Cogs: {i.COG_NAMES} | Version: {i.VERSION}")
            await ctx.message.add_reaction("✅")
        except commands.ExtensionNotFound:
            # The plugin could not be found
            pluginLog.error(f"{folder}.{plug}: not found (ExtensionNotFound)")
            await ctx.message.add_reaction("❌")
        except commands.ExtensionAlreadyLoaded:
            # The plugin was already loaded
            pluginLog.info(f"{folder}.{plug}: already loaded (ExtensionAlreadyLoaded)")
            await ctx.message.add_reaction("✅")
        except commands.NoEntryPointError:
            # The plugin does not have a setup function
            pluginLog.error(f"{folder}.{plug}: no setup function (NoEntryPointError)")
            await ctx.message.add_reaction("❌")
            await ctx.message.add_reaction("⚠️")
        except commands.ExtensionFailed:
            # The plugin setup function has an execution error
            pluginLog.error(f"{folder}.{plug}: execution error (ExtensionFailed)")
            await ctx.message.add_reaction("❌")
            await ctx.message.add_reaction("⚠️")
        except Exception as error:
            self.bot.unload_extension(f"{folder}.{plug}")
            pluginLog.error(f"{folder}.{plug}: variables not properly defined. Plugin unloaded.")
            await ctx.message.add_reaction("❌")
            await ctx.message.add_reaction("⚠️")

    @plugin.command(name="unload", description="Unload a plugin", usage="<plugin name>", aliases=["u"])
    @commands.is_owner()
    async def unload(self, ctx, plug):
        """
        Unload a plugin
        `unload_extension <https://discordpy.readthedocs.io/en/latest/ext/commands/api.html?highlight=unload_extension#discord.ext.commands.Bot.unload_extension>`
        :param ctx:
        :param str plug: Plugin name
        """
        try:
            folder = readINI("config.ini")["main"]["pluginFolder"]
            i = importlib.import_module(f"{folder}.{plug}")

            if i.REQUIRED:
                await ctx.message.add_reaction("⚠️")
                await ctx.send("Required plugins cannot be unloaded")
                return

            self.bot.unload_extension(f"{folder}.{plug}")
            pluginCol = connect()["applesauce"]["plugins"] # connect to DB
            pluginINFO = { "_id": plug, 
                            "plugin_name": i.PLUGIN_NAME,
                            "cog_names": i.COG_NAMES,
                            "version": i.VERSION,
                            "author": i.AUTHOR,
                            "description": i.DESCRIPTION,
                            "load_on_start": i.LOAD_ON_START, 
                            "required": i.REQUIRED,
                            "loaded": False }
            pluginCol.update_one({ "_id": plug }, { "$set": pluginINFO }, upsert=True)
            pluginLog.info(f"Unloaded: {plug} ({i.PLUGIN_NAME}) | Cogs: {i.COG_NAMES} | Version: {i.VERSION}")
            await ctx.message.add_reaction("✅")
        except commands.ExtensionNotLoaded:
            # The plugin was not found or unloaded
            pluginLog.error(f"{folder}.{plug}: unable to be found and unloaded. (ExtensionNotLoaded)")
            await ctx.message.add_reaction("❌")
        except Exception as error:
            pluginLog.error(f"{folder}.{plug}: unknown unloading plugin error.")
            await ctx.message.add_reaction("❌")
            await ctx.message.add_reaction("⚠️")

    @plugin.command(name="reload", description="Reload a plugin", usage="<plugin name>", aliases=["r"])
    @commands.is_owner()
    async def reload(self, ctx, plug):
        """
        Reload a plugin
        `reload_extension <https://discordpy.readthedocs.io/en/latest/ext/commands/api.html?highlight=reload_extension#discord.ext.commands.Bot.reload_extension>`
        :param ctx:
        :param str plug: Plugin name
        """
        try:
            folder = readINI("config.ini")["main"]["pluginFolder"]
            self.bot.reload_extension(f"{folder}.{plug}")
            i = importlib.import_module(f"{folder}.{plug}")
            pluginCol = connect()["applesauce"]["plugins"] # connect to DB
            pluginINFO = { "_id": plug, 
                            "plugin_name": i.PLUGIN_NAME,
                            "cog_names": i.COG_NAMES,
                            "version": i.VERSION,
                            "author": i.AUTHOR,
                            "description": i.DESCRIPTION,
                            "load_on_start": i.LOAD_ON_START, 
                            "required": i.REQUIRED,
                            "loaded": True }
            pluginCol.update_one({ "_id": plug }, { "$set": pluginINFO }, upsert=True)
            pluginLog.info(f"Reloaded: {plug} ({i.PLUGIN_NAME}) | Cogs: {i.COG_NAMES} | Version: {i.VERSION}")
            await ctx.message.add_reaction("✅")
        except commands.ExtensionNotLoaded:
            # The plugin doesn't exist
            pluginLog.error(f"{folder}.{plug}: not found (ExtensionNotLoaded)")
            await ctx.message.add_reaction("❌")
        except commands.ExtensionNotFound:
            # The plugin did exist at one point but now doesn't
            # Was probably loaded but than deleted
            pluginLog.info(f"{folder}.{plug}: not found (ExtensionNotFound)")
            await ctx.message.add_reaction("❌")
            await ctx.message.add_reaction("⚠️")
        except commands.NoEntryPointError:
            # The plugin does not have a setup function
            pluginLog.error(f"{folder}.{plug}: no setup function (NoEntryPointError)")
            await ctx.message.add_reaction("❌")
            await ctx.message.add_reaction("⚠️")
        except commands.ExtensionFailed:
            # The plugin setup function has an execution error
            pluginLog.error(f"{folder}.{plug}: execution error (ExtensionFailed)")
            await ctx.message.add_reaction("❌")
            await ctx.message.add_reaction("⚠️")
        except Exception as error:
            pluginLog.error(f"{folder}.{plug}: unknown reloading plugin error.")
            await ctx.message.add_reaction("❌")
            await ctx.message.add_reaction("⚠️")