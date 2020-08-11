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
        self._original_help_command = bot.help_command
        bot.help_command = SetupHelp()
        bot.help_command.cog = self

class SetupHelp(commands.MinimalHelpCommand):
    async def command_not_found(self, string):
        embed=discord.Embed(title="Command not found.", color=0xf84722)
        await self.context.send(embed=embed)

    async def subcommand_not_found(self, command, string):
        embed=discord.Embed(title="Subcommand not found.", color=0xf84722)
        await self.context.send(embed=embed)

    # async def send_cog_help(self, cog):

    # async def send_group_help(self, group):

    # async def send_command_help(self, command):

    async def send_bot_help(self, mapping):
        # get list of commands
        allCmds = []

        for command in set(self.context.bot.walk_commands()):
            try:
                await command.can_run(self.context)
                allCmds.append(str(command))
            except:
                pass

        allCmds = sorted(allCmds)
        enableCmds = []
        for item in allCmds:
            if " " not in item:
                enableCmds.append(item)

        enableString = commandList(enableCmds)
        embed=discord.Embed(title='Help', description=f'Specify a command to get further information `{prefix(self.context.guild.id)}help <command>`', color=0xc1c100)
        embed.add_field(name='Commands', value=f'{enableString}', inline=False)
        await self.context.send(embed=embed)
