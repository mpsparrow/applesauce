import os
import discord
from discord.ext import commands
from utils.checks import is_guild_enabled
from utils.database.actions import connect
from utils.config import readINI
from utils.prefix import prefix as getPrefix

class Help(commands.Cog):
    """
    Custom commands
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
            await ctx.send("a command")
        except Exception:
            await self.error(ctx)

    async def subcommand(self, ctx, subcommand, prefix):
        """
        subcommand embed
        :param ctx:
        :param subcommand: subcommand object
        :param str prefix: command prefix for guild
        """
        try:
            await ctx.send("a subcommand")
        except Exception:
            await self.error(ctx)

    async def group(self, ctx, group, prefix):
        """
        group embed
        :param ctx:
        :param group: group object
        :param str prefix: command prefix for guild
        """
        try:
            await ctx.send("a group")
        except Exception:
            await self.error(ctx)

    async def cog(self, ctx, cog, prefix):
        """
        cog embed
        :param ctx:
        :param cog: cog object
        :param str prefix: command prefix for guild
        """
        try:
            await ctx.send("a cog")
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
                embed=discord.Embed(title=pluginData["plugin_name"], description=pluginData["description"], color=0xc1c100)
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

                await ctx.send(embed=embed)
            else:
                await self.plugin_invalid(ctx)
        except Exception:
            await self.plugin_invalid(ctx)

    async def all(self, ctx, prefix):
        """
        all help embed
        :param ctx:
        :param str prefix: command prefix for guild
        """
        try:
            embed=discord.Embed(title="Help", 
                                description=f"`{prefix}help command <command>`\n`{prefix}help plugin <plugin>`\n`{prefix}help cog <cog>`\n\n**__Plugins__**", 
                                color=0xc1c100)

            pluginCol = connect()[readINI("config.ini")["MongoDB"]["database"]]["plugins"]
            folder = readINI("config.ini")["main"]["pluginFolder"]

            for plugin in next(os.walk(folder))[1]:
                # skips '__pycache__' folder
                if plugin == "__pycache__":
                    continue

                try:
                    pluginData = pluginCol.find_one({ "_id": plugin })
                    
                    if pluginData["guilds"][str(ctx.guild.id)] and pluginData["loaded"]:
                        cogStr = ""

                        for cog in pluginData["cog_names"]:
                            cogData = self.bot.get_cog(cog)
                            cogStr += f"`{cogData.qualified_name}`, "
                    
                        if cogStr.count("`") > 2:
                            embed.add_field(name=f"{plugin}", value=f"Cogs: {cogStr[:-2]}", inline=True)
                        else:
                            embed.add_field(name=f"{plugin}", value=f"Cog: {cogStr[:-2]}", inline=True)
                except TypeError:
                    # not a plugin
                    pass
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

    @commands.command(name="help", description="Help command", usage="<plugin/command>", aliases=["h"])
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
            itemSplit = helpItem.strip().split(" ")
            itemType = itemSplit[0].lower()

            if len(itemSplit) > 1:
                item = " ".join(itemSplit[1:])

                if itemType in ["command", "commands", "com", "group", "groups", "subcommand"]:
                    command = self.bot.get_command(item)

                    if command is not None:
                        await ctx.send("some command")
                    else:
                        await self.command_invalid(ctx)

                elif itemType in ["p", "plugin", "plugins", "plug"]:
                    pluginCol = connect()[readINI("config.ini")["MongoDB"]["database"]]["plugins"]
                    pluginData = pluginCol.find_one({ "_id": item })

                    if pluginData is not None:
                        await self.plugin(ctx, pluginData, prefix)
                    else:
                        await self.plugin_invalid(ctx)
                elif itemType in ["cog"]:
                    cog = self.bot.get_cog(item)

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