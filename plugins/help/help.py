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
        self.description = "" if description is None else description
        self.cogData = cogData
        self.cmds = {}

    def addCmd(self, cmd):
        """
        Store Cmd object
        :param Cmd cmd: Cmd object
        """
        self.cmds[cmd.name] = cmd

class Cmd():
    """
    Represents a command
    """
    def __init__(self, cmdtype: str):
        self.cmdtype = cmdtype

class Regular(Cmd):
    """
    Represents a regular command
    """
    def __init__(self, name, usage, description, cmd):
        Cmd.__init__(self, "Regular")
        self.name = name
        self.usage = "" if usage is None else usage
        self.description = "" if description is None else description
        self.cmd = cmd            

class Group(Cmd):
    """
    Represents a group command
    """
    def __init__(self, name, usage, description, cmd):
        Cmd.__init__(self, "Group")
        self.name = name
        self.usage = "" if usage is None else usage
        self.description = "" if description is None else description
        self.aliases = cmd.aliases
        self.cmd = cmd
        self.subcmds = {}

    def addSub(self, sub):
        """
        Stores Sub object
        :param Sub sub: Sub object
        """
        self.subcmds[sub.name] = sub

class Sub():
    """
    Represents a sub command in a group command
    """
    def __init__(self, base, name, usage, description, sub):
        self.base = base
        self.name = name
        self.usage = "" if usage is None else usage
        self.description = "" if description is None else description
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
        self.cog = None

    def addPlugin(self, plugin):
        """
        Stores Plugin object
        :param Plugin plugin: Plugin object
        """
        self.plugins[plugin.id] = plugin

    async def buildRegular(self, regular, cog, without_plugin=False):
        """
        Builds Regular object
        :param commands.Command regular: Regular command object
        :param Cog cog: Cog object
        :param bool without_plugin: Create without Plugin object
        """
        if without_plugin:
            self.cog.addCmd(Regular(regular.name, regular.usage, regular.description, regular))
        else:
            cog.addCmd(Regular(regular.name, regular.usage, regular.description, regular))

    async def buildGroup(self, group, cog, without_plugin=False):
        """
        Builds Group object
        :param commands.Command group: Group command object
        :param Cog cog: Cog object
        :param bool without_plugin: Create without Plugin object
        """
        if without_plugin:
            self.cog.addCmd(Group(group.qualified_name, group.usage, group.description, group))
        else:
            cog.addCmd(Group(group.qualified_name, group.usage, group.description, group))

    async def buildSub(self, sub, cog, without_plugin=False):
        """
        Builds Sub object
        :param commands.Command sub: Sub command object
        :param Cog cog: Cog object
        :param bool without_plugin: Create without Plugin object
        """
        if without_plugin:
            self.cog.cmds[sub.root_parent.name].addSub(Sub(sub.full_parent_name, sub.name, sub.usage, sub.description, sub))
        else:
            cog.cmds[sub.root_parent.name].addSub(Sub(sub.full_parent_name, sub.name, sub.usage, sub.description, sub))

    async def buildCmd(self, cmd, cog, without_plugin=False):
        """
        Builds Cmd object
        :param commands.Command cmd: Command object
        :param Cog cog: Cog object
        :param bool without_plugin: Create without Plugin object
        """
        if cmd.root_parent is not None:
            # subcommand
            await self.buildSub(cmd, cog, without_plugin)
        else:
            try:
                listCmds = cmd.commands
                # group
                await self.buildGroup(cmd, cog, without_plugin)
            except Exception:
                # command
                await self.buildRegular(cmd, cog, without_plugin)

    async def buildCogWithoutPlugin(self, cog):
        """
        Builds a full Cog without the Plugin object
        :param str cog: Cog object
        :return: Cog object
        """
        self.cog = Cog(cog.qualified_name, cog.description, cog)
        # Loops through all commands in cog
        for cmd in cog.walk_commands():
            # If ctx.author can run command
            try:
                await cmd.can_run(self.ctx)
            except commands.CommandError:
                continue

            # Build command object
            await self.buildCmd(cmd, cog, without_plugin=True)

    async def buildCog(self, cog, pluginData):
        """
        Build Cog object
        :param str cog: Cog name
        """
        cogData = self.bot.get_cog(cog)

        # Add Cog
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
                
    async def buildPlugin(self, plugin):
        """
        Build Plugin object
        :param str plugin: Plugin id
        """
        # Get plugin from database
        pluginData = self.pluginCol.find_one({ "_id": plugin })

        if pluginData is not None:
            # Plugin exist in database
            if pluginData["loaded"] and pluginData["guilds"][str(self.ctx.guild.id)]:
                # Plugin loaded and enabled
                
                # Add Plugin
                self.addPlugin(Plugin(pluginData["_id"], pluginData["plugin_name"], pluginData["description"], pluginData))

                # Loops through all cogs in plugin
                for cog in pluginData["cog_names"]:
                    # Build Cog object
                    await self.buildCog(cog, pluginData)

    async def buildAll(self):
        """
        Builds all Plugin objects
        """
        # Loops through all plugins in folder
        for plugin in next(os.walk(self.folder))[1]:
            # Skips '__pycache__' folder
            if plugin == "__pycache__":
                continue

            # Build Plugin object
            await self.buildPlugin(plugin)

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
        self.helpObject = None

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

    async def group(self, group):
        """
        Group command embed
        :param Group group: Group object
        """
        try:
            embed=discord.Embed(title=group.name, description=group.description, color=0xc1c100)
            embed.add_field(name="Usage", value=f"`{self.prefix}{group.name} {group.usage}`", inline=False)

            if len(group.aliases) > 0:
                aliases = ""
                for alias in group.aliases:
                    aliases += f"`{alias}`, "
                embed.add_field(name="Aliases", value=aliases[:-2], inline=False)

            if len(group.subcmds) > 0:
                subcmdStr = ""
                for subKey, sub in group.subcmds.items():
                    subcmdStr += f"`{sub.name}` - {sub.description}\n"
                embed.add_field(name="Sub Commands", value=subcmdStr, inline=False)
            embed.set_footer(text=f"Type: Group")
            await self.ctx.send(embed=embed)
        except Exception:
            await self.command_invalid()

    async def sub(self, sub):
        """
        Sub command embed
        :param Sub sub: Sub object
        """
        try:
            embed=discord.Embed(title=sub.name, description=sub.description, color=0xc1c100)
            embed.add_field(name="Usage", value=f"`{self.prefix}{sub.base} {sub.name} {sub.usage}`", inline=False)
            if len(sub.sub.aliases) > 0:
                aliases = ""
                for alias in sub.sub.aliases:
                    aliases += f"`{alias}`, "
                embed.add_field(name="Aliases", value=aliases[:-2])
            embed.set_footer(text=f"Type: Sub Command | Group: {sub.base}")
            await self.ctx.send(embed=embed)
        except Exception:
            await self.command_invalid()

    async def regular(self, command):
        """
        Regular command embed
        :param Regular command: Regular object
        """
        try:
            embed=discord.Embed(title=command.name, description=command.description, color=0xc1c100)
            embed.add_field(name="Usage", value=f"`{self.prefix}{command.name} {command.usage}`", inline=False)
            if len(command.cmd.aliases) > 0:
                aliases = ""
                for alias in command.cmd.aliases:
                    aliases += f"`{alias}`, "
                embed.add_field(name="Aliases", value=aliases[:-2])
            embed.set_footer(text=f"Type: Command")
            await self.ctx.send(embed=embed)
        except Exception:
            await self.command_invalid()

    async def command(self, name):
        """
        Command embeds
        :param str name: Name of command
        """
        try:
            cmd = self.bot.get_command(name)
            await self.helpObject.buildCogWithoutPlugin(cmd.cog)
            if " " in name:
                baseCmd = name.strip().split(" ")[0]
                cmdOb = self.helpObject.cog.cmds[cmd.root_parent.name].subcmds[cmd.name]
                await self.sub(cmdOb)
            else:
                cmdOb = self.helpObject.cog.cmds[cmd.name]
                classType = cmdOb.cmdtype
                if classType == "Group":
                    await self.group(cmdOb)
                elif classType == "Regular":
                    await self.regular(cmdOb)
        except Exception:
            await self.command_invalid()

    async def cog(self, name):
        """
        Cog embed
        :param str name: Name of cog
        """
        try:
            cog = self.bot.get_cog(name)
            await self.helpObject.buildCogWithoutPlugin(cog)
            cog = self.helpObject.cog

            embed=discord.Embed(title=cog.name, description=cog.description, color=0xc1c100)

            cmdStr = ""

            for cmdKey, cmd in cog.cmds.items():
                cmdStr += f"`{self.prefix}{cmd.name} {cmd.usage}` - {cmd.description}\n"
                
            if len(cmdStr) != 0:
                embed.add_field(name="Commands", value=cmdStr, inline=False)

            embed.set_footer(text=f"Type: Cog | ID: {cog.name}")
            await self.ctx.send(embed=embed)
        except Exception:
            await self.cog_invalid()

    async def plugin(self, name):
        """
        Plugin embed
        :param str name: Name of plugin
        """
        try:
            await self.helpObject.buildPlugin(name)
            plugin = self.helpObject.getPlugin(name)

            embed=discord.Embed(title=plugin.name, description=plugin.description, color=0xc1c100)

            cmdStr = ""
            cogStr = ""

            for cogKey, cog in plugin.cogs.items():
                cogStr += f"`{cog.name}`, "
                for cmdKey, cmd in cog.cmds.items():
                    cmdStr += f"`{cmd.name}`, "

            if len(cogStr) != 0:
                embed.add_field(name="Cogs", value=cogStr[:-2], inline=False)

            if len(cmdStr) != 0:
                embed.add_field(name="Commands", value=cmdStr[:-2], inline=False)

            embed.set_footer(text=f"Type: Plugin | ID: {plugin.id}")
            await self.ctx.send(embed=embed)
        except Exception:
            await self.plugin_invalid()

    async def all(self):
        """
        Main help
        """
        try:
            await self.helpObject.buildAll()
            embed=discord.Embed(title="Help", 
                                description=f"`{self.prefix}help command <command>`\n`{self.prefix}help plugin <plugin>`\n`{self.prefix}help cog <cog>`", 
                                color=0xc1c100)
            helpAll = self.helpObject.getAll()
            for pluginKey, plugin in helpAll.items():
                count = 0
                cogsStr = ""
                for cogKey, cog in plugin.cogs.items():
                    cogsStr += f"`{cog.name}`, "
                    count += 1

                if count == 1:
                    cogsStr = "Cog: " + cogsStr
                elif count > 1:
                    cogsStr = "Cogs: " + cogsStr
                else:
                    cogsStr = "No Cogs"

                embed.add_field(name=f"{plugin.name} ({plugin.id})", value=cogsStr[:-2], inline=False)
            await self.ctx.send(embed=embed)
        except Exception:
            await self.error()

    async def item_help(self):
        """
        Invalid help item type
        """
        embed=discord.Embed(title="Invalid Item", 
                            description=f"**Please Use**\n`{self.prefix}help command <command>`\n`{self.prefix}help plugin <plugin>`\n`{self.prefix}help cog <cog>`", 
                            color=0xf84722)
        await self.ctx.send(embed=embed)

    @commands.cooldown(1, 5, commands.BucketType.guild)
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
        self.helpObject = HelpBuilder(ctx, self.bot)

        try:
            if helpItem is None:
                # Display main help information is no helpItem is given
                await self.all()
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
                        # Is a command
                        await self.command(item)

                    elif itemType in ["p", "plugin", "plugins", "plug"]:
                        # Is a plugin
                        await self.plugin(item)

                    elif itemType in ["cog"]:
                        # Is a cog
                        await self.cog(item)
                    else:
                        # Invalid helpItem
                        await self.item_help()
                else:
                    # Incorrect amount of params given
                    await self.item_help()
        except Exception:
            await self.error()

    @commands.command(name="setup", description="Bot setup instructions")
    @commands.has_permissions(manage_guild=True)
    async def setup(self, ctx):
        """
        Setup instructions 
        :param ctx:
        """
        self.prefix = getPrefix(ctx.guild.id)
        embed=discord.Embed(title="Setup Instructions", 
                            description=f"**Prefix**: `{self.prefix}`\n**Help**: `{self.prefix}help`\n**Plugins**: Use `{self.prefix}p a` to manage plugins", 
                            color=0xc1c100)
        await ctx.send(embed=embed)