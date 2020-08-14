import os
import discord
from discord.ext import commands
from utils.checks import is_guild_enabled
from utils.database.actions import connect
from utils.config import readINI
from utils.prefix import prefix as getPrefix

class Plugin():
    """
    Represents a plugins
    """
    def __init__(self, idname, name, description, pluginData):
        self.id = idname
        self.name = name
        self.description = description
        self.pluginData = pluginData
        self.cogs = {}

    def addCog(self, cog):
        """
        Store Cog object
        """
        self.cogs[cog.name] = cog

class Cog():
    """
    Represents a cog
    """
    def __init__(self, name, description, cogData):
        self.name = name
        self.description = description
        self.cogData = cogData
        self.cmds = {}

    def addCmd(self, cmd):
        """
        Store Cmd object
        """
        self.cmds[cmd.name] = cmd

class Cmd():
    """
    Represents a command
    """
    pass

class Regular(Cmd):
    """
    Represents a regular command
    """
    def __init__(self, name, usage, description, cmd):
        self.name = name
        self.usage = usage
        self.description = description
        self.cmd = cmd

class Group(Cmd):
    """
    Represents a group command
    """
    def __init__(self, name, usage, description, cmd):
        self.name = name
        self.usage = usage
        self.description = description
        self.cmd = cmd
        self.subcmds = {}

    def addSub(self, sub):
        """
        Stores Sub object
        """
        self.subcmds[sub.name] = sub

class Sub():
    """
    Represents a sub command in a group
    """
    def __init__(self, base, name, usage, description, sub):
        self.base = base
        self.name = name
        self.usage = usage
        self.description = description
        self.sub = sub

class HelpBuilder():
    """
    Builds help command structure
    """
    def __init__(self, ctx, bot):
        self.ctx = ctx
        self.bot = bot

        self.pluginCol = connect()[readINI("config.ini")["MongoDB"]["database"]]["plugins"]
        self.folder = readINI("config.ini")["main"]["pluginFolder"]

        self.plugins = {}

    def addPlugin(self, plugin):
        """
        Stores Plugin object
        """
        self.plugins[plugin.id] = plugin

    async def buildRegular(self, regular, cog):
        """
        Builds Regular object
        :param commands.Command regular: Regular command object
        :param cog: Cog object
        """
        cog.addCmd(Regular(regular.name, regular.usage, regular.description, regular))

    async def buildGroup(self, group, cog):
        """
        Builds Group object
        :param commands.Command group: Group command object
        :param cog: Cog object
        """
        cog.addCmd(Group(group.qualified_name, group.usage, group.description, group))

    async def buildSub(self, sub, cog):
        """
        Builds Sub object
        :param commands.Command sub: Sub command object
        :param cog: Cog object
        """
        cog.cmds[sub.root_parent.name].addSub(Sub(sub.full_parent_name, sub.name, sub.usage, sub.description, sub))

    async def buildCmd(self, cmd, cog):
        """
        Builds Cmd object
        :param commands.Command cmd: Command object
        :param cog: Cog object
        """
        if cmd.root_parent is not None:
            # subcommand
            await self.buildSub(cmd, cog)
        else:
            try:
                listCmds = cmd.commands
                # group
                await self.buildGroup(cmd, cog)
            except Exception:
                # command
                await self.buildRegular(cmd, cog)
                
    async def build(self):
        """
        Builds Plugin object
        """
        # Loops through all plugins in folder
        for plugin in next(os.walk(readINI("config.ini")["main"]["pluginFolder"]))[1]:
            # Skips '__pycache__' folder
            if plugin == "__pycache__":
                continue

            # Get plugin from database
            pluginData = self.pluginCol.find_one({ "_id": plugin })

            if pluginData is None:
                # Plugin doesn't exist in database
                continue
            else:
                if not(pluginData["loaded"]) or not(pluginData["guilds"][str(self.ctx.guild.id)]):
                    continue

                # Plugin is in the database
                self.addPlugin(Plugin(pluginData["_id"], pluginData["plugin_name"], pluginData["description"], pluginData))

                # Loops through all cogs in plugin
                for cog in pluginData["cog_names"]:
                    cogData = self.bot.get_cog(cog)
                    self.plugins[pluginData["_id"]].addCog(Cog(cog, cogData.description, cogData))

                    # Loops through all commands in cog
                    for cmd in cogData.walk_commands():
                        # If ctx.author can run command
                        try:
                            await cmd.can_run(self.ctx)
                        except commands.CommandError:
                            continue

                        # Build command object
                        await self.buildCmd(cmd, self.plugins[pluginData["_id"]].cogs[cog])

    def getCmd(self, plugin, cog, cmd):
        """
        Get command object
        :param str plugin: Plugin name
        :param str cog: Cog name
        :param str cmd: Cmd name
        """
        if " " in cmd:
            group = cmd.strip().split(" ")[0]
            sub = cmd.strip().split(" ")[1]
            return self.plugins[plugin][cog][group][sub]

        return self.plugins[plugin][cog][cmd]
        
    def getCog(self, plugin, cog):
        """
        Get cog object
        :param str plugin: Plugin name
        :param str cog: Cog name
        """
        return self.plugins[plugin][cog]

    def getPlugin(self, plugin):
        """
        Get plugin object
        :param str plugin: Plugin name
        """
        return self.plugins[plugin]

    def getAll(self):
        """
        Get all plugin objects
        """
        return self.plugins

class Help(commands.Cog):
    """
    Help commands
    """
    def __init__(self, bot):
        self.bot = bot
        self.bot.remove_command("help")
        self.prefix = None
        self.ctx = None

    async def error(self):
        """
        generic error embed
        """
        embed=discord.Embed(title="Not found.", color=0xf84722)
        await self.ctx.send(embed=embed)

    async def command_invalid(self):
        """
        invalid command embed
        """
        embed=discord.Embed(title="Command not found.", color=0xf84722)
        await self.ctx.send(embed=embed)

    async def cog_invalid(self):
        """
        invalid cog embed
        """
        embed=discord.Embed(title="Cog not found.", color=0xf84722)
        await self.ctx.send(embed=embed)

    async def plugin_invalid(self):
        """
        invalid plugin embed
        """
        embed=discord.Embed(title="Plugin not found.", color=0xf84722)
        await self.ctx.send(embed=embed)

    async def command(self, name, helpObject):
        """
        command embed
        :param str name: Name of command
        :param HelpBuilder helpObject: Help building object
        """
        try:
            print("command")
            await helpObject.build()
            cmd = helpObject.getCmd(plugin, cog, name)
            print(cmd)
        except Exception as error:
            print(error)
            await self.command_invalid()

    async def cog(self, name, helpObject):
        """
        cog embed
        :param str name: Name of cog
        :param HelpBuilder helpObject: Help building object
        """
        try:
            await helpObject.build()
            cog = helpObject.getCog(plugin, name)
        except Exception as error:
            print(error)
            await self.cog_invalid()

    async def plugin(self, name, helpObject):
        """
        plugin embed
        :param str name: Name of plugin
        :param HelpBuilder helpObject: Help building object
        """
        try:
            await helpObject.build()
            plugin = helpObject.getPlugin(name)
        except Exception as error:
            print(error)
            await self.plugin_invalid()

    async def all(self, helpObject):
        """
        Main help
        :param HelpBuilder helpObject: Help building object
        """
        await helpObject.build()
        embed=discord.Embed(title="Help", 
                            description=f"`{self.prefix}help command <command>`\n`{self.prefix}help plugin <plugin>`\n`{self.prefix}help cog <cog>`", 
                            color=0xc1c100)
        helpAll = helpObject.getAll()
        for pluginKey, plugin in helpAll.items():
            cogsStr = ""
            for cogKey, cog in plugin.cogs.items():
                cogStr = f"  {cog.name}: "
                for cmdKey, cmd in cog.cmds.items():
                    cogStr += f"`{cmd.name}`, "
                cogsStr += f"{cogStr[:-2]}\n"
            embed.add_field(name=plugin.name, value=cogsStr, inline=False)
        await self.ctx.send(embed=embed)

    async def item_help(self):
        """
        Invalid help item type
        """
        embed=discord.Embed(title="Invalid Item", 
                            description=f"**Please Use**\n`{self.prefix}help command <command>`\n`{self.prefix}help plugin <plugin>`\n`{self.prefix}help cog <cog>`", 
                            color=0xf84722)
        await self.ctx.send(embed=embed)

    @commands.command(name="help", description="Help command", usage="<command/cog/plugin>", aliases=["h"])
    async def help(self, ctx, *, helpItem: str = None):
        """
        Help command
        :param ctx:
        :param str helpItem: item that needs help
        """
        # Get prefix for guild
        self.prefix = getPrefix(ctx.guild.id)
        self.ctx = ctx

        helpObject = HelpBuilder(ctx, self.bot)

        try:
            if helpItem is None:
                print("all 1")
                # Display main help information is no helpItem is given
                await self.all(helpObject)
            else:
                # helpItem given
                # Splits the tag from the rest of the helpItem input
                itemSplit = helpItem.strip().split(" ")
                itemType = itemSplit[0].lower()

                # If a tag and an item were given
                if len(itemSplit) > 1:
                    item = " ".join(itemSplit[1:])

                    # Checking what type of input it is that requires help
                    # Types: command/subcommand/group, cog, plugin
                    if itemType in ["command", "commands", "com", "group", "groups", "subcommand"]:
                        print("command 1")
                        # Is a command
                        await self.command(command, helpObject)

                    elif itemType in ["p", "plugin", "plugins", "plug"]:
                        print("plugin 1")
                        # Is a plugin
                        await self.plugin(item, helpObject)

                    elif itemType in ["cog"]:
                        print("cog 1")
                        # Is a cog
                        await self.cog(cog, helpObject)
                    else:
                        # Invalid helpItem
                        await self.item_help()
                else:
                    # Incorrect amount of params given
                    await self.item_help()
        except Exception as error:
            print(error)
            await self.error()

    @commands.command(name="setup", description="Bot setup instructions")
    @commands.has_permissions(manage_guild=True)
    async def setup(self, ctx):
        """
        Setup instructions 
        :param ctx:
        """
        embed=discord.Embed(title="Setup Instructions", 
                            description=f"**Prefix**: {getPrefix(ctx.guild.id)}\n**Help**: {getPrefix(ctx.guild.id)}help", 
                            color=0xc1c100)
        await ctx.send(embed=embed)