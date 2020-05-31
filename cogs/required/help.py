import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
from util import embed

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._original_help_command = bot.help_command
        bot.help_command = Help()
        bot.help_command.cog = self

class SetupHelp(commands.MinimalHelpCommand):
    async def command_not_found(self, string):
        await self.context.send(embed=embed.make_error_embed("Command not found"))

    async def subcommand_not_found(self, command, string):
        await self.context.send(embed=embed.make_error_embed("sub command"))

    async def send_cog_help(self, cog):
        await self.context.send(embed=embed.make_error_embed("Cog help"))

    async def send_group_help(self, group):
        await self.context.send(embed=embed.make_error_embed("Group help"))
        
    async def send_command_help(self, command):
        await self.context.send(embed=embed.make_error_embed("command help"))

    async def send_bot_help(self, mapping):
        await self.context.send(embed=embed.make_error_embed("bot help"))

def setup(bot):
    bot.add_cog(Help(bot))