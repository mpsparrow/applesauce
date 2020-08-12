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

nav_emotes = {
    "right": "➡️",
    "left": "⬅️",
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
    def __init__(self, name, version, enabled, loaded, hidden, description):
        self.name = name
        self.version = version
        self.enabled = enabled
        self.loaded = loaded
        self.hidden = hidden
        self.description = description

class PluginManager():
    """
        An object representing the plugin manager in discord.
        Used for reaction based navigation etc
    """
    def __init__(self, owner, verbose, bot, isBotOwner, guildID):
        self.owner = owner
        self.verbose = verbose
        self.bot = bot
        self.isBotOwner = isBotOwner,
        self.guildID = guildID

        self.pluginCol = connect()[readINI("config.ini")["MongoDB"]["database"]]["plugins"] # connect to DB
        self.folder = readINI("config.ini")["main"]["pluginFolder"]

        self.plugins = []
        self.loadPluginList()

        self.total_pages = math.ceil(len(self.plugins) / PLUGINS_PER_PAGE)
        self.current_page = 0
        self.selected_item = 0

        self.messageID = 0
        self.current_status = emote_reactions["blank"]

    def updateStatus(self, *newStatus):
        self.current_status = ""
        for status in newStatus:
            self.current_status += emote_reactions[status]

    def toggleLoad(self):
        try:
            plug = self.plugins[self.current_page * PLUGINS_PER_PAGE + self.selected_item]
            becomeLoaded = (plug.loaded != emote_reactions["loaded"])

            #self.bot.load_extension(f"{self.folder}.{plug.name}")
            i = importlib.import_module(f"{self.folder}.{plug.name}.plugininfo")

            if becomeLoaded:
                self.bot.load_extension(f"{self.folder}.{plug.name}")
                plug.loaded = emote_reactions["loaded"]
            else:
                if i.REQUIRED:
                    self.updateStatus("warning")
                    # await ctx.send("Required plugins cannot be unloaded")
                    return
                
                self.bot.unload_extension(f"{self.folder}.{plug.name}")
                plug.loaded = emote_reactions["unloaded"]

            pluginINFO = { "_id": plug.name, 
                            "plugin_name": i.PLUGIN_NAME,
                            "cog_names": i.COG_NAMES,
                            "version": i.VERSION,
                            "author": i.AUTHOR,
                            "description": i.DESCRIPTION,
                            "load_on_start": i.LOAD_ON_START, 
                            "required": i.REQUIRED,
                            "hidden": i.HIDDEN,
                            "loaded": True }
            self.pluginCol.update_one({ "_id": plug.name }, { "$set": pluginINFO }, upsert=True)
            pluginLog.info(f"Loaded: {plug.name} ({i.PLUGIN_NAME}) | Cogs: {i.COG_NAMES} | Version: {i.VERSION}")
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
            self.bot.unload_extension(f"{self.folder}.{plug.name}")
            pluginLog.error(f"{self.folder}.{plug.name}: variables not properly defined. Plugin unloaded.")
            pluginLog.error(error)
            self.updateStatus("failed", "warning")

    def reload(self):
        try:
            plug = self.plugins[self.current_page * PLUGINS_PER_PAGE + self.selected_item]
            # don't allow reloading of itself
            if plug.name == "plugins":
                pluginLog.error(f"{self.folder}.{plug.name}: not allowed to reload the reloading plugin >.>")
                self.updateStatus("failed")
                return

            self.bot.reload_extension(f"{self.folder}.{plug.name}")
            i = importlib.import_module(f"{self.folder}.{plug.name}.plugininfo")
            pluginINFO = { "_id": plug.name, 
                            "plugin_name": i.PLUGIN_NAME,
                            "cog_names": i.COG_NAMES,
                            "version": i.VERSION,
                            "author": i.AUTHOR,
                            "description": i.DESCRIPTION,
                            "load_on_start": i.LOAD_ON_START, 
                            "required": i.REQUIRED,
                            "hidden": i.HIDDEN,
                            "loaded": True }
            self.pluginCol.update_one({ "_id": plug.name }, { "$set": pluginINFO }, upsert=True)
            pluginLog.info(f"Reloaded: {plug.name} ({i.PLUGIN_NAME}) | Cogs: {i.COG_NAMES} | Version: {i.VERSION}")
            self.updateStatus("success")
        except commands.ExtensionNotLoaded as error:
            # The plugin doesn't exist
            pluginLog.error(f"{self.folder}.{plug.name}: not found (ExtensionNotLoaded)")
            pluginLog.error(error)
            self.updateStatus("failed")
        except commands.ExtensionNotFound as error:
            # The plugin did exist at one point but now doesn't
            # Was probably loaded but than deleted
            pluginLog.info(f"{self.folder}.{plug.name}: not found (ExtensionNotFound)")
            pluginLog.error(error)
            self.updateStatus("failed", "warning")
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
            pluginLog.error(f"{self.folder}.{plug.name}: unknown reloading plugin error.")
            pluginLog.error(error)
            self.updateStatus("failed", "warning")

    def toggleEnable(self):
        try:
            plug = self.plugins[self.current_page * PLUGINS_PER_PAGE + self.selected_item]
            becomeEnabled = (plug.enabled == emote_reactions["disabled"])
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
            pluginLog.error(f"{self.folder}.{plug.name}: unable to enable extension")
            pluginLog.error(error)
            self.updateStatus("failed")

    def up(self):
        self.selected_item -= 1
        if self.selected_item < 0:
            if self.current_page < self.total_pages - 1:
                self.selected_item = PLUGINS_PER_PAGE - 1
            else:
                self.selected_item = len(self.plugins) - (self.total_pages - 1) * PLUGINS_PER_PAGE - 1

    def down(self):
        self.selected_item += 1
        if self.selected_item >= PLUGINS_PER_PAGE or (self.current_page * PLUGINS_PER_PAGE) + self.selected_item >= len(self.plugins):
            self.selected_item = 0

    def next(self):
        self.current_page += 1
        self.selected_item = 0
        if self.current_page >= self.total_pages:
            self.current_page = 0

    def prev(self):
        self.current_page -= 1
        self.selected_item = 0
        if self.current_page < 0:
            self.current_page = self.total_pages - 1

    def makeEmbed(self):
        embed = discord.Embed(
            title = "Plugins",
            color = 0xc1c100
        )
        
        for i in range(PLUGINS_PER_PAGE):
            try:
                plugin = self.plugins[self.current_page * PLUGINS_PER_PAGE + i]
                if self.verbose:
                    embed.add_field(
                        name=f"{'‣ ' if i == self.selected_item else ''}{plugin.enabled}{plugin.loaded}{plugin.hidden} {plugin.name} (v{plugin.version})",
                        value=plugin.description,
                        inline=False
                    )
                else:
                    embed.add_field(
                        name=f"{'‣ ' if i == self.selected_item else ''}{plugin.enabled} {plugin.name}",
                        value=plugin.description,
                        inline=False
                    )

            except:
                break

        embed.set_footer(text=f"Latest status: {self.current_status}\t\t{self.current_page + 1}/{self.total_pages}")

        return embed

    def loadPluginList(self):
        if self.verbose and self.isBotOwner:
            for plug in next(os.walk(self.folder))[1]:
                # skips '__pycache__' folder
                if plug == "__pycache__":
                    continue

                try:
                    data = self.pluginCol.find_one({ "_id": plug })
                    loaded = emote_reactions["loaded"] if data["loaded"] else emote_reactions["shown"]
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

                    self.plugins.append(Plugin(data['_id'], data['version'], enabledGuild, loaded, hidden, data['description']))
                except TypeError:
                    # not in database
                    i = importlib.import_module(f"{self.folder}.{plug}.plugininfo")
                    hidden = emote_reactions["hidden"] if i.HIDDEN else emote_reactions["shown"]
                    self.plugins.append(Plugin(plug, i.VERSION, emote_reactions["blank"], emote_reactions["blank"], hidden, i.DESCRIPTION))
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

                self.plugins.append(Plugin(x['_id'], "", enabledGuild, emote_reactions["blank"], emote_reactions["blank"], x['description']))


class Plugins(commands.Cog):
    """
    Plugin management commands
    """
    def __init__(self, bot):
        self.bot = bot
        self.activeObject = None

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        message = reaction.message
        if message.id != self.activeObject.messageID:
            return

        if user == self.bot.user:
            return

        if user.id != self.activeObject.owner.id:
            return

        if reaction.me:
            if reaction.emoji == nav_emotes["left"]:
                self.activeObject.prev()
                await reaction.remove(user)

            if reaction.emoji == nav_emotes["right"]:
                self.activeObject.next()
                await reaction.remove(user)

            if reaction.emoji == nav_emotes["up"]:
                self.activeObject.up()
                await reaction.remove(user)

            if reaction.emoji == nav_emotes["down"]:
                self.activeObject.down()
                await reaction.remove(user)

            if reaction.emoji == nav_emotes["enable"]:
                self.activeObject.toggleEnable()
                await reaction.remove(user)

            if reaction.emoji == nav_emotes["reload"]:
                self.activeObject.reload()
                await reaction.remove(user)

            if reaction.emoji == nav_emotes["load"]:
                self.activeObject.toggleLoad()
                await reaction.remove(user)

        embed = self.activeObject.makeEmbed()
        await message.edit(embed=embed)

    @commands.group(name="plugin", description="Plugin management", usage="<action>", aliases=["p", "plug"], invoked_subcommand=True)
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
        self.activeObject = PluginManager(
            ctx.author, 
            show_unloaded, 
            self.bot,
            await self.bot.is_owner(ctx.author),
            ctx.guild.id
        )

        msg = await ctx.send(embed=self.activeObject.makeEmbed())

        if self.activeObject.total_pages > 1:
            await msg.add_reaction(nav_emotes["left"])
            await msg.add_reaction(nav_emotes["right"])

        await msg.add_reaction(nav_emotes["up"])
        await msg.add_reaction(nav_emotes["down"])
        await msg.add_reaction(nav_emotes["enable"])
        await msg.add_reaction(nav_emotes["reload"])

        if show_unloaded:
            await msg.add_reaction(nav_emotes["load"])

        self.activeObject.messageID = msg.id

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
        try:
            folder = readINI("config.ini")["main"]["pluginFolder"]
            self.bot.load_extension(f"{folder}.{plug}")
            i = importlib.import_module(f"{folder}.{plug}.plugininfo")
            pluginCol = connect()[readINI("config.ini")["MongoDB"]["database"]]["plugins"] # connect to DB
            pluginINFO = { "_id": plug, 
                            "plugin_name": i.PLUGIN_NAME,
                            "cog_names": i.COG_NAMES,
                            "version": i.VERSION,
                            "author": i.AUTHOR,
                            "description": i.DESCRIPTION,
                            "load_on_start": i.LOAD_ON_START, 
                            "required": i.REQUIRED,
                            "hidden": i.HIDDEN,
                            "loaded": True }
            pluginCol.update_one({ "_id": plug }, { "$set": pluginINFO }, upsert=True)
            pluginLog.info(f"Loaded: {plug} ({i.PLUGIN_NAME}) | Cogs: {i.COG_NAMES} | Version: {i.VERSION}")
            await ctx.message.add_reaction(emote_reactions["success"])
        except commands.ExtensionNotFound as error:
            # The plugin could not be found
            pluginLog.error(f"{folder}.{plug}: not found (ExtensionNotFound)")
            pluginLog.error(error)
            await ctx.message.add_reaction(emote_reactions["failed"])
        except commands.ExtensionAlreadyLoaded as error:
            # The plugin was already loaded
            pluginLog.info(f"{folder}.{plug}: already loaded (ExtensionAlreadyLoaded)")
            pluginLog.error(error)
            await ctx.message.add_reaction(emote_reactions["success"])
        except commands.NoEntryPointError as error:
            # The plugin does not have a setup function
            pluginLog.error(f"{folder}.{plug}: no setup function (NoEntryPointError)")
            pluginLog.error(error)
            await ctx.message.add_reaction(emote_reactions["failed"])
            await ctx.message.add_reaction(emote_reactions["warning"])
        except commands.ExtensionFailed as error:
            # The plugin setup function has an execution error
            pluginLog.error(f"{folder}.{plug}: execution error (ExtensionFailed)")
            pluginLog.error(error)
            await ctx.message.add_reaction(emote_reactions["failed"])
            await ctx.message.add_reaction(emote_reactions["warning"])
        except Exception as error:
            self.bot.unload_extension(f"{folder}.{plug}")
            pluginLog.error(f"{folder}.{plug}: variables not properly defined. Plugin unloaded.")
            pluginLog.error(error)
            await ctx.message.add_reaction(emote_reactions["failed"])
            await ctx.message.add_reaction(emote_reactions["warning"])

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
            i = importlib.import_module(f"{folder}.{plug}.plugininfo")

            if i.REQUIRED:
                await ctx.message.add_reaction(emote_reactions["warning"])
                await ctx.send("Required plugins cannot be unloaded")
                return

            self.bot.unload_extension(f"{folder}.{plug}")
            pluginCol = connect()[readINI("config.ini")["MongoDB"]["database"]]["plugins"] # connect to DB
            pluginINFO = { "_id": plug, 
                            "plugin_name": i.PLUGIN_NAME,
                            "cog_names": i.COG_NAMES,
                            "version": i.VERSION,
                            "author": i.AUTHOR,
                            "description": i.DESCRIPTION,
                            "load_on_start": i.LOAD_ON_START, 
                            "required": i.REQUIRED,
                            "hidden": i.HIDDEN,
                            "loaded": False }
            pluginCol.update_one({ "_id": plug }, { "$set": pluginINFO }, upsert=True)
            pluginLog.info(f"Unloaded: {plug} ({i.PLUGIN_NAME}) | Cogs: {i.COG_NAMES} | Version: {i.VERSION}")
            await ctx.message.add_reaction(emote_reactions["success"])
        except commands.ExtensionNotLoaded as error:
            # The plugin was not found or unloaded
            pluginLog.error(f"{folder}.{plug}: unable to be found and unloaded. (ExtensionNotLoaded)")
            pluginLog.error(error)
            await ctx.message.add_reaction(emote_reactions["failed"])
        except Exception as error:
            pluginLog.error(f"{folder}.{plug}: unknown unloading plugin error.")
            pluginLog.error(error)
            await ctx.message.add_reaction(emote_reactions["failed"])
            await ctx.message.add_reaction(emote_reactions["warning"])

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

            # don't allow reloading of itself
            if plug == "plugins":
                pluginLog.error(f"{folder}.{plug}: not allowed to reload the reloading plugin >.>")
                await ctx.message.add_reaction(emote_reactions["failed"])
                return

            self.bot.reload_extension(f"{folder}.{plug}")
            i = importlib.import_module(f"{folder}.{plug}.plugininfo")
            pluginCol = connect()[readINI("config.ini")["MongoDB"]["database"]]["plugins"] # connect to DB
            pluginINFO = { "_id": plug, 
                            "plugin_name": i.PLUGIN_NAME,
                            "cog_names": i.COG_NAMES,
                            "version": i.VERSION,
                            "author": i.AUTHOR,
                            "description": i.DESCRIPTION,
                            "load_on_start": i.LOAD_ON_START, 
                            "required": i.REQUIRED,
                            "hidden": i.HIDDEN,
                            "loaded": True }
            pluginCol.update_one({ "_id": plug }, { "$set": pluginINFO }, upsert=True)
            pluginLog.info(f"Reloaded: {plug} ({i.PLUGIN_NAME}) | Cogs: {i.COG_NAMES} | Version: {i.VERSION}")
            await ctx.message.add_reaction(emote_reactions["success"])
        except commands.ExtensionNotLoaded as error:
            # The plugin doesn't exist
            pluginLog.error(f"{folder}.{plug}: not found (ExtensionNotLoaded)")
            pluginLog.error(error)
            await ctx.message.add_reaction(emote_reactions["failed"])
        except commands.ExtensionNotFound as error:
            # The plugin did exist at one point but now doesn't
            # Was probably loaded but than deleted
            pluginLog.info(f"{folder}.{plug}: not found (ExtensionNotFound)")
            pluginLog.error(error)
            await ctx.message.add_reaction(emote_reactions["failed"])
            await ctx.message.add_reaction(emote_reactions["warning"])
        except commands.NoEntryPointError as error:
            # The plugin does not have a setup function
            pluginLog.error(f"{folder}.{plug}: no setup function (NoEntryPointError)")
            pluginLog.error(error)
            await ctx.message.add_reaction(emote_reactions["failed"])
            await ctx.message.add_reaction(emote_reactions["warning"])
        except commands.ExtensionFailed as error:
            # The plugin setup function has an execution error
            pluginLog.error(f"{folder}.{plug}: execution error (ExtensionFailed)")
            pluginLog.error(error)
            await ctx.message.add_reaction(emote_reactions["failed"])
            await ctx.message.add_reaction(emote_reactions["warning"])
        except Exception as error:
            pluginLog.error(f"{folder}.{plug}: unknown reloading plugin error.")
            pluginLog.error(error)
            await ctx.message.add_reaction(emote_reactions["failed"])
            await ctx.message.add_reaction(emote_reactions["warning"])

    @plugin.command(name="enable", description="Enable a plugin in a guild", usage="<plugin name>", aliases=["e"])
    @commands.has_permissions(manage_guild=True)
    async def enable(self, ctx, plug, guildID=None):
        """
        Enable a plugin in a guild
        :param ctx:
        :param str plug: Plugin name
        """
        try:
            folder = readINI("config.ini")["main"]["pluginFolder"]
            i = importlib.import_module(f"{folder}.{plug}.plugininfo")
            pluginCol = connect()[readINI("config.ini")["MongoDB"]["database"]]["plugins"] # connect to DB

            if guildID is not None and await self.bot.is_owner(ctx.author):
                validID = True
                if len(str(guildID)) != 18:
                    validID = False

                try:
                    int(guildID)
                except ValueError:
                    validID = False

                if validID:
                    pluginCol.update_one({ "_id": plug }, { "$set": { f"guilds.{str(guildID)}": True }}, upsert=True)
                    pluginLog.info(f"Enabled: {plug} ({i.PLUGIN_NAME}) | Guild: {str(guildID)} | Cogs: {i.COG_NAMES}")
                    await ctx.message.add_reaction(emote_reactions["success"])
                else:
                    pluginLog.error(f"{folder}.{plug}: owner invalid guildID for enabling extension")
                    await ctx.message.add_reaction(emote_reactions["failed"])
                    await ctx.message.add_reaction(emote_reactions["warning"])
            else:
                if i.HIDDEN:
                    if await self.bot.is_owner(ctx.author):
                        pluginCol.update_one({ "_id": plug }, { "$set": { f"guilds.{str(ctx.guild.id)}": True }}, upsert=True)
                        pluginLog.info(f"Enabled: {plug} ({i.PLUGIN_NAME}) | Guild: {str(ctx.guild.id)} | Cogs: {i.COG_NAMES}")
                        await ctx.message.add_reaction(emote_reactions["success"])
                    else:
                        pluginLog.error(f"{folder}.{plug}: unable to enable hidden extension")
                        await ctx.message.add_reaction(emote_reactions["failed"])
                else:
                    pluginCol.update_one({ "_id": plug }, { "$set": { f"guilds.{str(ctx.guild.id)}": True }}, upsert=True)
                    pluginLog.info(f"Enabled: {plug} ({i.PLUGIN_NAME}) | Guild: {str(ctx.guild.id)} | Cogs: {i.COG_NAMES}")
                    await ctx.message.add_reaction(emote_reactions["success"])
        except Exception as error:
            pluginLog.error(f"{folder}.{plug}: unable to enable extension")
            pluginLog.error(error)
            await ctx.message.add_reaction(emote_reactions["failed"])


    @plugin.command(name="disable", description="Disable a plugin in a guild", usage="<plugin name>", aliases=["d"])
    @commands.has_permissions(manage_guild=True)
    async def disable(self, ctx, plug, guildID=None):
        """
        Disable a plugin in a guild
        :param ctx:
        :param str plug: Plugin name
        """
        try:
            folder = readINI("config.ini")["main"]["pluginFolder"]
            i = importlib.import_module(f"{folder}.{plug}.plugininfo")
            pluginCol = connect()[readINI("config.ini")["MongoDB"]["database"]]["plugins"] # connect to DB

            if guildID is not None and await self.bot.is_owner(ctx.author):
                validID = True
                if len(str(guildID)) != 18:
                    validID = False

                try:
                    int(guildID)
                except ValueError:
                    validID = False

                if validID:
                    pluginCol.update_one({ "_id": plug }, { "$set": { f"guilds.{str(guildID)}": False }}, upsert=True)
                    pluginLog.info(f"Disabled: {plug} ({i.PLUGIN_NAME}) | Guild: {str(guildID)} | Cogs: {i.COG_NAMES}")
                    await ctx.message.add_reaction(emote_reactions["success"])
                else:
                    pluginLog.error(f"{folder}.{plug}: owner invalid guildID for disabling extension")
                    await ctx.message.add_reaction(emote_reactions["failed"])
                    await ctx.message.add_reaction(emote_reactions["warning"])
            else:
                if i.HIDDEN:
                    if await self.bot.is_owner(ctx.author):
                        pluginCol.update_one({ "_id": plug }, { "$set": { f"guilds.{str(ctx.guild.id)}": False }}, upsert=True)
                        pluginLog.info(f"Disabled: {plug} ({i.PLUGIN_NAME}) | Guild: {str(ctx.guild.id)} | Cogs: {i.COG_NAMES}")
                        await ctx.message.add_reaction(emote_reactions["success"])
                    else:
                        pluginLog.error(f"{folder}.{plug}: unable to disable hidden extension")
                        await ctx.message.add_reaction(emote_reactions["failed"])
                else:
                    pluginCol.update_one({ "_id": plug }, { "$set": { f"guilds.{str(ctx.guild.id)}": False }}, upsert=True)
                    pluginLog.info(f"Disabled: {plug} ({i.PLUGIN_NAME}) | Guild: {str(ctx.guild.id)} | Cogs: {i.COG_NAMES}")
                    await ctx.message.add_reaction(emote_reactions["success"])
        except Exception as error:
            pluginLog.error(f"{folder}.{plug}: unable to disable extension")
            pluginLog.error(error)
            await ctx.message.add_reaction(emote_reactions["failed"])