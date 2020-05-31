import discord
from discord.ext import commands
from discord.ext.commands import has_permissions

class Help(commands.Cog):
    def __init__(self, bot):
        self._original_help_command = bot.help_command
        bot.help_command = SetupHelp()
        bot.help_command.cog = self

class SetupHelp(commands.MinimalHelpCommand):
    async def command_not_found(self, string):
        await self.context.send("Command not found")

    async def subcommand_not_found(self, command, string):
        await self.context.send("sub command")

    async def send_cog_help(self, cog):
        await self.context.send("Cog help")

    async def send_group_help(self, group):
        await self.context.send("Group help")
        
    async def send_command_help(self, command):
        await self.context.send("command help")

    async def send_bot_help(self, mapping):
        await self.context.send("bot help")

def setup(bot):
    bot.add_cog(Help(bot))