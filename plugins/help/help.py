import discord
from discord.ext import commands
from utils.checks import is_guild_enabled
from utils.database.actions import connect
from utils.config import readINI
from utils.prefix import prefix

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

    async def command(self, ctx, command):
        """
        command embed
        :param ctx:
        :param command: command object
        """
        try:
            await ctx.send("a command")
        except Exception:
            await self.error(ctx)

    async def subcommand(self, ctx, subcommand):
        """
        subcommand embed
        :param ctx:
        :param subcommand: subcommand object
        """
        try:
            await ctx.send("a subcommand")
        except Exception:
            await self.error(ctx)

    async def group(self, ctx, group):
        """
        group embed
        :param ctx:
        :param group: group object
        """
        try:
            await ctx.send("a group")
        except Exception:
            await self.error(ctx)

    async def cog(self, ctx, cog):
        """
        cog embed
        :param ctx:
        :param cog: cog object
        """
        try:
            await ctx.send("a cog")
        except Exception:
            await self.error(ctx)

    async def plugin(self, ctx, pluginData):
        """
        plugin embed
        :param ctx:
        :param plugin: plugin data from db
        """
        try:
            await ctx.send("a plugin")
        except Exception:
            await self.error(ctx)

    async def all(self, ctx):
        """
        all help embed
        :param ctx:
        """
        try:
            """
            embed=discord.Embed(title="Help", description="", color=0xc1c100)
            embed.add_field(name="", value="", inline=False)
            await ctx.send(embed=embed)
            """
            await ctx.send("main help")
        except Exception:
            await self.error(ctx)

    @commands.command(name="help", description="Help command", usage="<plugin/command>", aliases=["h"])
    async def help(self, ctx, *, helpItem: str=None):
        """
        Help command
        :param ctx:
        :param str helpItem: item that needs help
        """
        if helpItem is None:
            # display main help information
            await self.all(ctx)
        else:
            command = self.bot.get_command(helpItem)
            cog = self.bot.get_cog(helpItem)

            if command is not None:
                # is a command/subcommand/group
                if command.parent is not None:
                    # must be a subcommand
                    await self.subcommand(command)
                await self.command(command)
            elif cog is not None:
                # is a cog
                await self.cog(ctx, cog)
            else:
                # either a plugin or isn't anything
                pluginCol = connect()[readINI("config.ini")["MongoDB"]["database"]]["plugins"]
                pluginData = pluginCol.find_one({ "_id": helpItem })

                if pluginData is not None:
                    # plugin
                    await self.plugin(ctx, pluginData)
                else:
                    # who knows what it is then
                    await self.error(ctx)