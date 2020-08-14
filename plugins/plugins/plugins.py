import os
import discord
import pymongo
import importlib
import math
from discord.ext import commands
from discord.ext.commands import has_permissions
from utils.database.actions import connect
from utils.logger import pluginLog
from utils.config import readINI
from utils.interactive import InteractiveEmbed

# Emotes used to display the status of operations
emote_reactions = { 
    "failed": "❌",
    "success": "✅",
    "warning": "⚠️",
    "loaded": "📥",
    "unloaded": "📤",
    "enabled": "✅",
    "disabled": "❌",
    "hidden": "❔",
    "shown": "⬛",
    "blank": "⬛"
}

# Emotes used for navigation
nav_emotes = {
    "left": "⬅️",
    "right": "➡️",
    "up": "⬆️",
    "down": "⬇️",
    "enable": "🔘",
    "load": "📦",
    "reload": "🔄"
}

PLUGINS_PER_PAGE = 8

class Plugin():
    """
    Represents a plugin
    """
    def __init__(self, name, plugin_name, version, enabled, loaded, hidden, description):
        self.name = name
        self.plugin_name = plugin_name
        self.version = version
        self.enabled = enabled
        self.loaded = loaded
        self.hidden = hidden
        self.description = description

class PluginManager(InteractiveEmbed):
    """
        An object representing the plugin manager in discord.
        Used for reaction based navigation etc
    """
    def __init__(self, parent, ctx, verbose, isBotOwner):
        reactions = list(nav_emotes.values())
        if not verbose:
            reactions = reactions[:-2]
         
        super(PluginManager, self).__init__(parent.bot, ctx, 60.0)

        self.parent = parent
        self.owner = ctx.author
        self.verbose = verbose
        self.isBotOwner = isBotOwner
        self.guildID = ctx.guild.id

        self.pluginCol = connect()[readINI("config.ini")["MongoDB"]["database"]]["plugins"] # connect to DB
        self.folder = readINI("config.ini")["main"]["pluginFolder"]

        self.plugins = []
        self.loadPluginList()

        self.total_pages = math.ceil(len(self.plugins) / PLUGINS_PER_PAGE)
        self.current_page = 0
        self.selected_item = 0

        self.messageHandle = None
        self.current_status = [emote_reactions["blank"]]

    def additional_checks(self, reaction, user):
        return self.isBotOwner

    async def add_navigation(self, message):
        if self.total_pages > 1:
            await message.add_reaction(nav_emotes["left"])
            await message.add_reaction(nav_emotes["right"])

        await message.add_reaction(nav_emotes["down"])
        await message.add_reaction(nav_emotes["up"])
        await message.add_reaction(nav_emotes["enable"])

        if self.verbose:
            await message.add_reaction(nav_emotes["reload"])
            await message.add_reaction(nav_emotes["load"])

    # Returns a plugin matching the name
    def getPluginByName(self, name: str) -> Plugin:
        for plugin in self.plugins:
            if plugin.name == name:
                return plugin

        return None

    # Updates the current, latest status of the manager
    def updateStatus(self, *newStatus):
        self.current_status.clear()
        for status in newStatus:
            self.current_status.append(emote_reactions[status])

    def toggleLoad(self, pluginOverride: str = None, loadOverride: bool = None):
        """
        Loads/Unloads the currently selected plugin depending on its state
        :param str pluginOverride: Forces the function to use the specified plugin
        :param bool loadOverride: Forces the function to either load or unload
        """
        try:
            if pluginOverride is None:
                plug = self.plugins[self.current_page * PLUGINS_PER_PAGE + self.selected_item]
            else:
                plug = self.getPluginByName(pluginOverride)

            if loadOverride is None:
                becomeLoaded = (plug.loaded != emote_reactions["loaded"])
            else:
                becomeLoaded = loadOverride

            i = importlib.import_module(f"{self.folder}.{plug.name}.plugininfo")

            if becomeLoaded:
                self.parent.bot.load_extension(f"{self.folder}.{plug.name}")
                plug.loaded = emote_reactions["loaded"]
                loadedDB = True
            else:
                if i.REQUIRED:
                    self.updateStatus("warning")
                    return
                
                self.parent.bot.unload_extension(f"{self.folder}.{plug.name}")
                plug.loaded = emote_reactions["unloaded"]
                loadedDB = False

            pluginINFO = { "_id": plug.name, 
                            "plugin_name": i.PLUGIN_NAME,
                            "cog_names": i.COG_NAMES,
                            "version": i.VERSION,
                            "author": i.AUTHOR,
                            "description": i.DESCRIPTION,
                            "load_on_start": i.LOAD_ON_START, 
                            "required": i.REQUIRED,
                            "hidden": i.HIDDEN,
                            "loaded": loadedDB }
            self.pluginCol.update_one({ "_id": plug.name }, { "$set": pluginINFO }, upsert=True)
            pluginLog.info(f"{'Loaded' if loadedDB else 'Unloaded'}: {plug.name} ({i.PLUGIN_NAME}) | Cogs: {i.COG_NAMES} | Version: {i.VERSION}")
            self.updateStatus("success")
        except commands.ExtensionNotFound as error:
            # The plugin could not be found
            pluginLog.error(f"{self.folder}.{plug.name}: not found (ExtensionNotFound)")
            pluginLog.error(error)
            self.updateStatus("failed")
        except commands.ExtensionAlreadyLoaded as error:
            # The plugin was already loaded
            pluginLog.info(f"{self.folder}.{plug.name}: already loaded (ExtensionAlreadyLoaded)")
            pluginLog.error(error)
            self.updateStatus("failed")
        except commands.ExtensionNotLoaded as error:
            # The plugin doesn't exist
            pluginLog.error(f"{self.folder}.{plug.name}: not found (ExtensionNotLoaded)")
            pluginLog.error(error)
            self.updateStatus("failed")
        except commands.NoEntryPointError as error:
            # The plugin does not have a setup function
            pluginLog.error(f"{self.folder}.{plug.name}: no setup function (NoEntryPointError)")
            pluginLog.error(error)
            self.updateStatus("failed", "warning")
        except commands.ExtensionFailed as error:
            # The plugin setup function has an execution error
            pluginLog.error(f"{self.folder}.{plug.name}: execution error (ExtensionFailed)")
            pluginLog.error(error)
            self.updateStatus("failed", "warning")
        except Exception as error:
            self.parent.bot.unload_extension(f"{self.folder}.{plug.name}")
            pluginLog.error(f"{self.folder}.{plug.name}: variables not properly defined. Plugin unloaded.")
            pluginLog.error(error)
            self.updateStatus("failed", "warning")

    def reload(self, pluginOverride: str = None):
        """
        Reloads the currently selected plugin
        param: str pluginOverride: Forces the function to reload the specified plugin
        """
        try:
            if pluginOverride is None:
                plug = self.plugins[self.current_page * PLUGINS_PER_PAGE + self.selected_item]
            else:
                plug = self.getPluginByName(pluginOverride)

            # don't allow reloading of itself
            if plug.name == "plugins":
                pluginLog.error(f"{self.folder}.{plug.name}: not allowed to reload the reloading plugin >.>")
                self.updateStatus("failed")
                return

            self.parent.bot.reload_extension(f"{self.folder}.{plug.name}")
            i = importlib.import_module(f"{self.folder}.{plug.name}.plugininfo")
            pluginLog.info(f"Reloaded: {plug.name} ({plug.plugin_name}) | Cogs: {i.COG_NAMES} | Version: {i.VERSION}")
            self.updateStatus("success")
        except commands.ExtensionNotLoaded as error:
            # The plugin doesn't exist
            pluginLog.error(f"{self.folder}.{plug.name}: not found (ExtensionNotLoaded)")
            pluginLog.error(error)
            self.pluginCol.update_one({ "_id": plug.name }, { "$set": { "loaded": False } }, upsert=True)
            self.updateStatus("failed")
        except commands.ExtensionNotFound as error:
            # The plugin did exist at one point but now doesn't
            # Was probably loaded but than deleted
            pluginLog.info(f"{self.folder}.{plug.name}: not found (ExtensionNotFound)")
            pluginLog.error(error)
            self.pluginCol.update_one({ "_id": plug.name }, { "$set": { "loaded": False } }, upsert=True)
            self.updateStatus("failed", "warning")
        except commands.NoEntryPointError as error:
            # The plugin does not have a setup function
            pluginLog.error(f"{self.folder}.{plug.name}: no setup function (NoEntryPointError)")
            pluginLog.error(error)
            self.pluginCol.update_one({ "_id": plug.name }, { "$set": { "loaded": False } }, upsert=True)
            self.updateStatus("failed", "warning")
        except commands.ExtensionFailed as error:
            # The plugin setup function has an execution error
            pluginLog.error(f"{self.folder}.{plug.name}: execution error (ExtensionFailed)")
            pluginLog.error(error)
            self.pluginCol.update_one({ "_id": plug.name }, { "$set": { "loaded": False } }, upsert=True)
            self.updateStatus("failed", "warning")
        except Exception as error:
            pluginLog.error(f"{self.folder}.{plug.name}: unknown reloading plugin error.")
            pluginLog.error(error)
            self.updateStatus("failed", "warning")

    def toggleEnable(self, pluginOverride: str = None, enableOverride: bool = None):
        """
        Enabled/Disables the currently selected plugin depending on its current state
        param: str pluginOverride: Forces the function to use the specified plugin
        param: bool enableOverride: Forces the function to either enable or disable the plugin
        """
        try:
            if pluginOverride is None:
                plug = self.plugins[self.current_page * PLUGINS_PER_PAGE + self.selected_item]
            else:
                plug = self.getPluginByName(pluginOverride)

            if enableOverride is None:
                becomeEnabled = (plug.enabled == emote_reactions["disabled"])
            else:
                becomeEnabled = enableOverride
                   
            i = importlib.import_module(f"{self.folder}.{plug.name}.plugininfo")
            if self.guildID is not None and self.isBotOwner:
                validID = True
                if len(str(self.guildID)) != 18:
                    validID = False

                try:
                    int(self.guildID)
                except ValueError:
                    validID = False

                if validID:
                    self.pluginCol.update_one({ "_id": plug.name }, { "$set": { f"guilds.{str(self.guildID)}": becomeEnabled }}, upsert=True)
                    pluginLog.info(f"{'Enabled' if becomeEnabled else 'Disabled'}: {plug.name} ({i.PLUGIN_NAME}) | Guild: {str(self.guildID)} | Cogs: {i.COG_NAMES}")
                    plug.enabled = emote_reactions["enabled"] if becomeEnabled else emote_reactions["disabled"]
                    self.updateStatus("success")
                else:
                    pluginLog.error(f"{self.folder}.{plug.name}: owner invalid guildID for enabling extension")
                    self.updateStatus("failed", "warning")
            else:
                if i.HIDDEN:
                    if self.isBotOwner:
                        self.pluginCol.update_one({ "_id": plug.name }, { "$set": { f"guilds.{str(self.guildID)}": becomeEnabled }}, upsert=True)
                        pluginLog.info(f"{'Enabled' if becomeEnabled else 'Disabled'}: {plug.name} ({i.PLUGIN_NAME}) | Guild: {str(self.guildID)} | Cogs: {i.COG_NAMES}")
                        plug.enabled = emote_reactions["enabled"] if becomeEnabled else emote_reactions["disabled"]
                        self.updateStatus("success")
                    else:
                        pluginLog.error(f"{self.folder}.{plug.name}: unable to enable hidden extension")
                        self.updateStatus("failed")
                else:
                    self.pluginCol.update_one({ "_id": plug }, { "$set": { f"guilds.{str(self.guildID)}": becomeEnabled }}, upsert=True)
                    pluginLog.info(f"{'Enabled' if becomeEnabled else 'Disabled'}: {plug.name} ({i.PLUGIN_NAME}) | Guild: {str(self.guildID)} | Cogs: {i.COG_NAMES}")
                    plug.enabled = emote_reactions["enabled"] if becomeEnabled else emote_reactions["disabled"]
                    self.updateStatus("success")
        except Exception as error:
            pluginLog.error(f"{self.folder}.{plug.name}: unable to enable/disable extension")
            pluginLog.error(error)
            self.updateStatus("failed")

    def up(self):
        """
        Moves the slection cursor up
        """
        self.selected_item -= 1
        if self.selected_item < 0:
            if self.current_page < self.total_pages - 1:
                self.selected_item = PLUGINS_PER_PAGE - 1
            else:
                self.selected_item = len(self.plugins) - (self.total_pages - 1) * PLUGINS_PER_PAGE - 1

    def down(self):
        """
        Moves the selection cursor down
        """
        self.selected_item += 1
        if self.selected_item >= PLUGINS_PER_PAGE or (self.current_page * PLUGINS_PER_PAGE) + self.selected_item >= len(self.plugins):
            self.selected_item = 0

    def next(self):
        """
        Goes to the next page
        """
        self.current_page += 1
        self.selected_item = 0
        if self.current_page >= self.total_pages:
            self.current_page = 0

    def prev(self):
        """
        Goes to the previous page
        """
        self.current_page -= 1
        self.selected_item = 0
        if self.current_page < 0:
            self.current_page = self.total_pages - 1

    async def on_reaction(self, reaction, user):
        # Prev page
            if reaction.emoji == nav_emotes["left"]:
                self.prev()
                await reaction.remove(user)

            # Next page
            if reaction.emoji == nav_emotes["right"]:
                self.next()
                await reaction.remove(user)

            # Cursor up
            if reaction.emoji == nav_emotes["up"]:
                self.up()
                await reaction.remove(user)

            # Cursor down
            if reaction.emoji == nav_emotes["down"]:
                self.down()
                await reaction.remove(user)

            # Enable/Disable plugin
            if reaction.emoji == nav_emotes["enable"]:
                self.toggleEnable()
                await reaction.remove(user)

            if self.verbose:
                # Reload plugin
                if reaction.emoji == nav_emotes["reload"]:
                    self.reload()
                    await reaction.remove(user)

                # Load/Unload plugin
                if reaction.emoji == nav_emotes["load"]:
                    self.toggleLoad()
                    await reaction.remove(user)

    def make_embed(self):
        """
        Creates a new embed from current information
        """
        embed = discord.Embed(
            title = "Plugins",
            color = 0xc1c100
        )
        
        for i in range(PLUGINS_PER_PAGE):
            try:
                plugin = self.plugins[self.current_page * PLUGINS_PER_PAGE + i]
                if self.verbose:
                    embed.add_field(
                        name=f"{'‣ ' if i == self.selected_item else ''}{plugin.enabled}{plugin.loaded}{plugin.hidden} {plugin.plugin_name} ({plugin.name} v{plugin.version})",
                        value=plugin.description,
                        inline=False
                    )
                else:
                    embed.add_field(
                        name=f"{'‣ ' if i == self.selected_item else ''}{plugin.enabled} {plugin.plugin_name}",
                        value=plugin.description,
                        inline=False
                    )

            except Exception:
                break

        embed.set_footer(text=f"Latest status: {''.join(self.current_status)}\t\t{self.current_page + 1}/{self.total_pages}")

        return embed

    def loadPluginList(self):
        """
        Loads all present plugins into the plugin array
        """
        if self.verbose and self.isBotOwner:
            for plug in next(os.walk(self.folder))[1]:
                # skips '__pycache__' folder
                if plug == "__pycache__":
                    continue

                try:
                    data = self.pluginCol.find_one({ "_id": plug })
                    loaded = emote_reactions["loaded"] if data["loaded"] else emote_reactions["unloaded"]
                    hidden = emote_reactions["hidden"] if data["hidden"] else emote_reactions["shown"]

                    # checks if plugin is enabled in guild
                    try:
                        isEnabled = data["guilds"][str(self.guildID)]
                        if isEnabled:
                            enabledGuild = emote_reactions["enabled"]
                        else:
                            enabledGuild = emote_reactions["disabled"]
                    except Exception:
                        enabledGuild = emote_reactions["disabled"]

                    self.plugins.append(Plugin(data['_id'], data['plugin_name'], data['version'], enabledGuild, loaded, hidden, data['description']))
                except TypeError:
                    try:
                        # not in database
                        i = importlib.import_module(f"{self.folder}.{plug}.plugininfo")
                        hidden = emote_reactions["hidden"] if i.HIDDEN else emote_reactions["shown"]
                        self.plugins.append(Plugin(plug, i.PLUGIN_NAME, i.VERSION, emote_reactions["blank"], emote_reactions["blank"], hidden, i.DESCRIPTION))
                    except ModuleNotFoundError:
                        # not a real plugin
                        pass
        else:
            for x in self.pluginCol.find({ "loaded": True, "hidden": False }):
                # checks if plugin is enabled in guild
                try:
                    isEnabled = x["guilds"][str(self.guildID)]
                    if isEnabled:
                        enabledGuild = emote_reactions["enabled"]
                    else:
                        enabledGuild = emote_reactions["disabled"]
                except Exception:
                    enabledGuild = emote_reactions["disabled"]

                self.plugins.append(Plugin(x['_id'], x['plugin_name'], "", enabledGuild, emote_reactions["blank"], emote_reactions["blank"], x['description']))


class Plugins(commands.Cog):
    """
    Plugin management commands
    """
    def __init__(self, bot):
        self.bot = bot
        self.activeObjects = {}

    async def createActiveObject(self, ctx, show_unloaded: bool = False):
        """
        Creates a new PluginManager and makes it the active object
        """
        if ctx.guild.id in self.activeObjects:
            await self.activeObjects[ctx.guild.id].close_embed()

        self.activeObjects[ctx.guild.id] = PluginManager(
            self,
            ctx, 
            show_unloaded,
            await self.bot.is_owner(ctx.author)
        )
        await self.activeObjects[ctx.guild.id].show_embed()

    @commands.group(name="plugin", description="Group for plugin management commands", usage="<subcommand>", aliases=["p", "plug"], invoked_subcommand=True)
    @commands.has_permissions(manage_guild=True)
    async def plugin(self, ctx):
        """
        Command group for plugin management
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

        # Make new active object
        await self.createActiveObject(ctx, show_unloaded)

    @plugin.command(name="info", description="List all loaded plugins", usage="<plugin name>", aliases=["i", "information"])
    @commands.has_permissions(manage_guild=True)
    async def info(self, ctx, plug, show_full: bool=False):
        """
        List information about a specific plugin
        :param ctx:
        :param str plug: Plugin name
        """
        pluginCol = connect()[readINI("config.ini")["MongoDB"]["database"]]["plugins"] # connect to DB
        folder = readINI("config.ini")["main"]["pluginFolder"]

        try:
            data = pluginCol.find_one({ "_id": plug })

            if data["loaded"] or await self.bot.is_owner(ctx.author):
                # checks if plugin is enabled in guild
                try:
                    isEnabled = data["guilds"][str(ctx.guild.id)]
                    if isEnabled:
                        enabledGuild = emote_reactions["enabled"]
                    else:
                        enabledGuild = emote_reactions["disabled"]
                except Exception:
                    enabledGuild = emote_reactions["disabled"]

                if await self.bot.is_owner(ctx.author) and show_full:
                    loaded = emote_reactions["loaded"] if data["loaded"] else emote_reactions["unloaded"]
                    hidden = emote_reactions["hidden"] if data["hidden"] else ""
                    embed=discord.Embed(title=f"{data['plugin_name']} {enabledGuild}{loaded}{hidden}", description=data["description"], color=0xc1c100)
                    embed.add_field(name=f"Version", 
                                    value=data["version"], inline=True)
                    load_on_start = emote_reactions["enabled"] if data["load_on_start"] else emote_reactions["disabled"]
                    embed.add_field(name=f"Load On Start", 
                                    value=load_on_start, inline=True)
                    required = emote_reactions["enabled"] if data["required"] else emote_reactions["disabled"]
                    embed.add_field(name=f"Required", 
                                    value=required, inline=True)
                    embed.add_field(name=f"ID Name", 
                                    value=data["_id"], inline=True)
                    cogString = ""
                    for cog in data["cog_names"]:
                        cogString += f"`{cog}`, "
                    embed.add_field(name=f"Cogs", 
                                    value=cogString[:-2], inline=True)
                    embed.set_footer(text=f"Created by {data['author']}")
                else:
                    embed=discord.Embed(title=f"{data['plugin_name']} {enabledGuild}", description=data["description"], color=0xc1c100)
                    embed.add_field(name=f"ID Name", 
                                    value=data["_id"], inline=False)
                await ctx.send(embed=embed)
        except TypeError:
            # not in database
            if await self.bot.is_owner(ctx.author) and show_full:
                i = importlib.import_module(f"{folder}.{plug}.plugininfo")
                hidden = emote_reactions["hidden"] if i.HIDDEN else ""
                embed=discord.Embed(title=f"{plug} {hidden} (never loaded)", description=i.DESCRIPTION, color=0xc1c100)
                embed.add_field(name=f"Version", 
                                value=i.VERSION, inline=True)
                load_on_start = emote_reactions["enabled"] if i.LOAD_ON_START else emote_reactions["disabled"]
                embed.add_field(name=f"Load On Start", 
                                value=load_on_start, inline=True)
                required = emote_reactions["enabled"] if i.REQUIRED else emote_reactions["disabled"]
                embed.add_field(name=f"Required", 
                                value=required, inline=True)
                embed.add_field(name=f"ID Name", 
                                value=plug, inline=True)
                cogString = ""
                for cog in i.COG_NAMES:
                    cogString += f"`{cog}`, "
                embed.add_field(name=f"Cogs", 
                                value=cogString[:-2], inline=True)
                embed.set_footer(text=f"Created by {i.AUTHOR}")
                await ctx.send(embed=embed)
            else:
                i = importlib.import_module(f"{folder}.{plug}.plugininfo")
                embed=discord.Embed(title=f"{plug} (never loaded)", description=i.DESCRIPTION, color=0xc1c100)
                embed.add_field(name=f"ID Name", 
                                value=plug, inline=False)
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
        # Create new active object (this won't be rendered)
        if ctx.guild.id not in self.activeObjects:
            await self.createActiveObject(ctx)

        # Force load the plugin
        self.activeObjects[ctx.guild.id].toggleLoad(plug, True)

        # Fetch status emotes and react
        for status in self.activeObjects[ctx.guild.id].current_status:
            await ctx.message.add_reaction(status)

        # Update embed
        await self.activeObjects[ctx.guild.id].updateEmbed()


    @plugin.command(name="unload", description="Unload a plugin", usage="<plugin name>", aliases=["u"])
    @commands.is_owner()
    async def unload(self, ctx, plug):
        """
        Unload a plugin
        `unload_extension <https://discordpy.readthedocs.io/en/latest/ext/commands/api.html?highlight=unload_extension#discord.ext.commands.Bot.unload_extension>`
        :param ctx:
        :param str plug: Plugin name
        """
        # Create new active object (this won't be rendered)
        if ctx.guild.id not in self.activeObjects:
            await self.createActiveObject(ctx)

        # Force unload the plugin
        self.activeObjects[ctx.guild.id].toggleLoad(plug, False)

        # Fetch status emotes and react
        for status in self.activeObjects[ctx.guild.id].current_status:
            await ctx.message.add_reaction(status)

        # Update embed
        await self.activeObjects[ctx.guild.id].updateEmbed()

    @plugin.command(name="reload", description="Reload a plugin", usage="<plugin name>", aliases=["r"])
    @commands.is_owner()
    async def reload(self, ctx, plug):
        """
        Reload a plugin
        `reload_extension <https://discordpy.readthedocs.io/en/latest/ext/commands/api.html?highlight=reload_extension#discord.ext.commands.Bot.reload_extension>`
        :param ctx:
        :param str plug: Plugin name
        """
        # Create new active object (this won't be rendered)
        if ctx.guild.id not in self.activeObjects:
            await self.createActiveObject(ctx)

        # Force reload the plugin
        self.activeObjects[ctx.guild.id].reload(plug)

        # Fetch status emotes and react
        for status in self.activeObjects[ctx.guild.id].current_status:
            await ctx.message.add_reaction(status)

        # Update embed
        await self.activeObjects[ctx.guild.id].updateEmbed()

    @plugin.command(name="enable", description="Enable a plugin in a guild", usage="<plugin name>", aliases=["e"])
    @commands.has_permissions(manage_guild=True)
    async def enable(self, ctx, plug, guildID=None):
        """
        Enable a plugin in a guild
        :param ctx:
        :param str plug: Plugin name
        """
        # Create new active object (this won't be rendered)
        if ctx.guild.id not in self.activeObjects:
            await self.createActiveObject(ctx)

        # Force enable the plugin
        self.activeObjects[ctx.guild.id].toggleEnable(plug, True)

        # Fetch status emotes and react
        for status in self.activeObjects[ctx.guild.id].current_status:
            await ctx.message.add_reaction(status)
        
        # Update embed
        await self.activeObjects[ctx.guild.id].updateEmbed()


    @plugin.command(name="disable", description="Disable a plugin in a guild", usage="<plugin name>", aliases=["d"])
    @commands.has_permissions(manage_guild=True)
    async def disable(self, ctx, plug, guildID=None):
        """
        Disable a plugin in a guild
        :param ctx:
        :param str plug: Plugin name
        """
        # Create new active object (this won't be rendered)
        if ctx.guild.id not in self.activeObjects:
            await self.createActiveObject(ctx)

        # Force disable the plugin
        self.activeObjects[ctx.guild.id].toggleEnable(plug, False)

        # Fetch status emotes and react
        for status in self.activeObjects[ctx.guild.id].current_status:
            await ctx.message.add_reaction(status)

        # Update embed
        await self.activeObjects[ctx.guild.id].updateEmbed()