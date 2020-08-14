import os
import discord
from discord.ext import commands
from utils.checks import is_guild_enabled
from utils.database.actions import connect
from utils.config import readINI
from utils.prefix import prefix as getPrefix

class Help(commands.Cog):
    """
    Help commands
    """
    def __init__(self, bot):
        self.bot = bot
        self.bot.remove_command("help")

    async def error(self, ctx):
        """
        generic error embed
        :param ctx:
        """
        embed=discord.Embed(title="Not found.", color=0xf84722)
        await ctx.send(embed=embed)

    async def command_invalid(self, ctx):
        """
        invalid command embed
        :param ctx:
        """
        embed=discord.Embed(title="Command not found.", color=0xf84722)
        await ctx.send(embed=embed)

    async def cog_invalid(self, ctx):
        """
        invalid cog embed
        :param ctx:
        """
        embed=discord.Embed(title="Cog not found.", color=0xf84722)
        await ctx.send(embed=embed)

    async def plugin_invalid(self, ctx):
        """
        invalid plugin embed
        :param ctx:
        """
        embed=discord.Embed(title="Plugin not found.", color=0xf84722)
        await ctx.send(embed=embed)

    async def command(self, ctx, command, prefix):
        """
        command embed
        :param ctx:
        :param command: command object
        :param str prefix: command prefix for guild
        """
        try:
            if command.enabled and not command.hidden:
                embed=discord.Embed(title=command.name, description=command.description, color=0xc1c100)

                # Displays command usage
                if command.usage is None:
                    embed.add_field(name="Usage", value=f"`{prefix}{command.name}`", inline=False)
                else:
                    embed.add_field(name="Usage", value=f"`{prefix}{command.name} {command.usage}`", inline=False)

                # Add in aliases if they exist
                if len(command.aliases) != 0:
                    aliasStr = ""
                    for alias in command.aliases:
                        aliasStr += f"`{alias}`, "

                    embed.add_field(name="Aliases", value=aliasStr[:-2], inline=False)
                embed.set_footer(text="Type: Command")
                await ctx.send(embed=embed)
            else:
                await self.command_invalid(ctx)
        except Exception:
            await self.command_invalid(ctx)

    async def subcommand(self, ctx, subcommand, prefix):
        """
        subcommand embed
        :param ctx:
        :param subcommand: subcommand object
        :param str prefix: command prefix for guild
        """
        try:
            if subcommand.enabled and not subcommand.hidden:
                embed=discord.Embed(title=subcommand.qualified_name, description=subcommand.description, color=0xc1c100)

                # Displays subcommand usage
                if subcommand.usage is None:
                    embed.add_field(name="Usage", value=f"`{prefix}{subcommand.qualified_name}`", inline=False)
                else:
                    embed.add_field(name="Usage", value=f"`{prefix}{subcommand.qualified_name} {subcommand.usage}`", inline=False)

                # Add in aliases if they exist
                if len(subcommand.aliases) != 0:
                    aliasStr = ""
                    for alias in subcommand.aliases:
                        aliasStr += f"`{alias}`, "

                    embed.add_field(name="Aliases", value=aliasStr[:-2], inline=False)
                embed.set_footer(text="Type: Subcommand")
                await ctx.send(embed=embed)
            else:
                await self.command_invalid(ctx)
        except Exception:
            await self.command_invalid(ctx)

    async def group(self, ctx, group, prefix):
        """
        group embed
        :param ctx:
        :param group: group object
        :param str prefix: command prefix for guild
        """
        try:
            if group.enabled and not group.hidden:
                embed=discord.Embed(title=group.qualified_name, description=group.description, color=0xc1c100)

                # Displays command usage
                if group.usage is None:
                    embed.add_field(name="Usage", value=f"`{prefix}{group.qualified_name} <subcommand>`", inline=False)
                else:
                    embed.add_field(name="Usage", value=f"`{prefix}{group.qualified_name} {group.usage}`", inline=False)

                # Add aliases if they exist
                if len(group.aliases) != 0:
                    aliasStr = ""
                    for alias in group.aliases:
                        aliasStr += f"`{alias}`, "

                    embed.add_field(name="Aliases", value=aliasStr[:-2], inline=False)

                subcommandStr = ""

                for subcommand in group.commands:
                    if subcommand.usage is None:
                        subcommandStr += f"`{sumcommand.name}`\n"
                    else:
                        subcommandStr += f"`{subcommand.name} {subcommand.usage}`\n"
                    
                embed.add_field(name="Subcommands", value=subcommandStr, inline=False)

                embed.set_footer(text="Type: Group")
                await ctx.send(embed=embed)
            else:
                await self.command_invalid(ctx)
        except Exception:
            await self.command_invalid(ctx)

    async def cog(self, ctx, cog, prefix):
        """
        cog embed
        :param ctx:
        :param cog: cog object
        :param str prefix: command prefix for guild
        """
        try:
            embed=discord.Embed(title=f"{cog.qualified_name}", description=cog.description, color=0xc1c100)
            comStr = ""
            
            for command in cog.walk_commands():
                # checks if subcommand
                if " " in command.qualified_name:
                    continue

                # checks if command is hidden or disabled
                if command.hidden and not command.enabled:
                    continue
                
                # can user run the command
                try:
                    await command.can_run(ctx)
                except commands.CommandError:
                    # cannot run
                    continue
                
                if command.usage is not None:
                    comStr += f"`{prefix}{command.name} {command.usage}` - {command.description}\n"
                else:
                    comStr += f"`{prefix}{command.name}` - {command.description}\n"

            embed.add_field(name=f"Commands", value=comStr, inline=False)
            embed.set_footer(text="Type: Cog")
            await ctx.send(embed=embed)
        except Exception:
            await self.error(ctx)

    async def plugin(self, ctx, pluginData, prefix):
        """
        plugin embed
        :param ctx:
        :param plugin: plugin data from db
        :param str prefix: command prefix for guild
        """
        try:
            if pluginData["guilds"][str(ctx.guild.id)] and pluginData["loaded"]:
                embed=discord.Embed(title=f"{pluginData['plugin_name']}", description=pluginData["description"], color=0xc1c100)
                for cog in pluginData["cog_names"]:
                    cogData = self.bot.get_cog(cog)
                    comStr = ""

                    for command in cogData.walk_commands():
                        # checks if subcommand
                        if " " in command.qualified_name:
                            continue
                        
                        # can user run the command
                        try:
                            await command.can_run(ctx)
                        except commands.CommandError:
                            # cannot run
                            continue
                        
                        if command.usage is not None:
                            comStr += f"`{prefix}{command.name} {command.usage}` - {command.description}\n"
                        else:
                            comStr += f"`{prefix}{command.name}` - {command.description}\n"
                    if len(comStr) > 0:
                        embed.add_field(name=f"Cog: {cogData.qualified_name}", value=comStr, inline=False)

                embed.set_footer(text="Type: Plugin")
                await ctx.send(embed=embed)
            else:
                await self.plugin_invalid(ctx)
        except Exception:
            await self.plugin_invalid(ctx)

    async def all(self, ctx, prefix, show_all: bool = False):
        """
        all help embed
        :param ctx:
        :param str prefix: command prefix for guild
        :param bool show_all: Show all hidden cogs
        """
        try:
            pluginCol = connect()[readINI("config.ini")["MongoDB"]["database"]]["plugins"]
            folder = readINI("config.ini")["main"]["pluginFolder"]

            helpStr = ""

            for plugin in next(os.walk(folder))[1]:
                # skips '__pycache__' folder
                if plugin == "__pycache__":
                    continue

                try:
                    pluginData = pluginCol.find_one({ "_id": plugin })

                    cogStr = ""

                    if show_all and pluginData["loaded"]:
                        for cog in pluginData["cog_names"]:
                            cogData = self.bot.get_cog(cog)
                            cogStr += f"`{cogData.qualified_name}`, "
                    
                        if cogStr.count("`") > 2:
                            helpStr += f"**{plugin}** | Cogs: {cogStr[:-2]}\n"
                        else:
                            helpStr += f"**{plugin}** | Cog: {cogStr[:-2]}\n"
                    elif pluginData["guilds"][str(ctx.guild.id)] and pluginData["loaded"]:
                        for cog in pluginData["cog_names"]:
                            cogData = self.bot.get_cog(cog)
                            cogStr += f"`{cogData.qualified_name}`, "
                    
                        if cogStr.count("`") > 2:
                            helpStr += f"**{plugin}** | Cogs: {cogStr[:-2]}\n"
                        else:
                            helpStr += f"**{plugin}** | Cog: {cogStr[:-2]}\n"
                except TypeError:
                    # not a plugin
                    pass
            embed=discord.Embed(title="Help", 
                                description=f"`{prefix}help command <command>`\n`{prefix}help plugin <plugin>`\n`{prefix}help cog <cog>`\n\n**__Plugins__**\n{helpStr}", 
                                color=0xc1c100)
            await ctx.send(embed=embed)
        except Exception:
            await self.error(ctx)

    async def item_help(self, ctx, prefix):
        """
        item help
        :param ctx:
        :param str prefix: command prefix for guild
        """
        embed=discord.Embed(title="Invalid Item", 
                            description=f"**Please Use**\n`{prefix}help command <command>`\n`{prefix}help plugin <plugin>`\n`{prefix}help cog <cog>`", 
                            color=0xf84722)
        await ctx.send(embed=embed)

    @commands.command(name="helpall", description="Help command that shows all plugins (hidden or not)", aliases=["ha"])
    @commands.is_owner()
    async def helpall(self, ctx):
        """
        Help command (displays all plugins)
        :param ctx:
        :param str helpItem: item that needs help
        """
        prefix = getPrefix(ctx.guild.id)
        await self.all(ctx, prefix, show_all=True)

    @commands.command(name="help", description="Help command", usage="<command/cog/plugin>", aliases=["h"])
    async def help(self, ctx, *, helpItem: str=None):
        """
        Help command
        :param ctx:
        :param str helpItem: item that needs help
        """
        prefix = getPrefix(ctx.guild.id)

        if helpItem is None:
            # display main help information
            await self.all(ctx, prefix)
        else:
            # Splits the tag from the rest of the helpItem input
            itemSplit = helpItem.strip().split(" ")
            itemType = itemSplit[0].lower()

            # If a tag and an item were given
            if len(itemSplit) > 1:
                item = " ".join(itemSplit[1:])

                # Checking what type of input it is that requires help
                # Types: command, cog, plugin
                # command needs to then check for: command, subcommand, group
                if itemType in ["command", "commands", "com", "group", "groups", "subcommand"]:
                    # Is some type of command
                    command = self.bot.get_command(item)

                    # can user run the command
                    try:
                        await command.can_run(ctx)
                    except commands.CommandError:
                        # cannot run
                        await self.command_invalid(ctx)
                        return

                    try:
                        # What type of command is it? subcommand, command, group
                        if command.root_parent is not None:
                            # subcommand
                            await self.subcommand(ctx, command, prefix)
                        else:
                            try:
                                x = command.commands
                                # group
                                await self.group(ctx, command, prefix)
                            except Exception:
                                # command
                                await self.command(ctx, command, prefix)
                    except Exception as error:
                        await self.command_invalid(ctx)

                elif itemType in ["p", "plugin", "plugins", "plug"]:
                    # Is a plugin
                    pluginCol = connect()[readINI("config.ini")["MongoDB"]["database"]]["plugins"]
                    pluginData = pluginCol.find_one({ "_id": item })

                    # Checks if plugin exists
                    if pluginData is not None:
                        if pluginData["guilds"][str(ctx.guild.id)]:
                            await self.plugin(ctx, pluginData, prefix)
                        else:
                            await self.plugin_invalid(ctx)
                    else:
                        await self.plugin_invalid(ctx)
                elif itemType in ["cog"]:
                    # Is a cog
                    cog = self.bot.get_cog(item)

                    # Checks if cog exists
                    if cog is not None:
                        await self.cog(ctx, cog, prefix)
                    else:
                        await self.cog_invalid(ctx)
                else:
                    # itemType didn't match
                    await self.item_help(ctx, prefix)
            else:
                # need at least 2 params
                await self.item_help(ctx, prefix)

    @commands.command(name="setup", description="Bot setup instructions")
    @commands.has_permissions(manage_guild=True)
    async def setup(self, ctx):
        """
        Setup instructions 
        :param ctx:
        """
        embed=discord.Embed(title="Setup Instructions", 
                            description=f"Still need to fill this in.... Prefix: {getPrefix(ctx.guild.id)}", 
                            color=0xc1c100)
        await ctx.send(embed=embed)