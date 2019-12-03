import discord
from discord.ext import commands
from discord.ext.commands import has_permissions

class SetupHelp(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._original_help_command = bot.help_command
        bot.help_command = Help()
        bot.help_command.cog = self

class Help(commands.MinimalHelpCommand):
    async def send_command_help(self, command):
        # removes aliases if there are none
        if command.aliases == []:
            alias = ""
        else:
            alias = f'\n**Aliases:**  {command.aliases}'
            
        embed=discord.Embed(title=f'{command.name}', description=f'**Description:**  {command.description}\n**Usage:**  `{command.usage}`{alias}', color=0xc1c100)
        await self.context.send(embed=embed)

    async def send_bot_help(self, mapping):
        embed=discord.Embed(title='Help', description=f'All commands. Use `help command` for more info.', color=0xc1c100)

        # get list of commands
        cmds = []
        for cog, cog_commands in mapping.items():
            cmds = cmds + cog_commands

        # put commands in alphabetical order
        newCmds = []
        for item in cmds:
            newCmds.append(str(item))
        newCmds = sorted(newCmds)

        # combine commands into string for output
        commandStr = ''
        for cmd in newCmds:
            commandStr += '``' + str(cmd) + '`` '

        # add all commands to embed and message it
        embed.add_field(name='Commands', value=f'{commandStr}', inline=False)
        await self.context.send(embed=embed)

def setup(bot):
    bot.add_cog(SetupHelp(bot))
