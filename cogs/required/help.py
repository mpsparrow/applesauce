'''
Custom help command
'''
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
from cogs.utils import configloader, config

class SetupHelp(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._original_help_command = bot.help_command
        bot.help_command = Help()
        bot.help_command.cog = self

class Help(commands.MinimalHelpCommand):
    async def command_not_found(self, string):
        await self.context.send(embed=embed.make_error_embed("Command not found"))

    async def subcommand_not_found(self, command, string):
        await self.context.send(embed=embed.make_error_embed("Command not found"))

    async def send_cog_help(self, cog):
        await self.context.send(embed=embed.make_error_embed("Command not found"))

    async def send_group_help(self, group):
        await self.context.send(embed=embed.make_error_embed("Command not found"))

    async def send_command_help(self, command):
        config = configloader.configLoad('guildconfig.json') # loads guildconfig.json
        try:
            prefix = config[str(self.context.guild.id)]['prefix']
        except:
            config2 = configloader.configLoad('config.json')
            prefix = config2['main']['prefix']

        try:
            randomVar = config[str(self.context.guild.id)]["Commands"][str(command.name)] # gets true/false value of command for guild
            if randomVar == True: # if command is enabled in guild
                # creates list of aliases for command
                alias = 'None'
                if command.aliases != []:
                    for i in range(len(command.aliases)):
                        if i == len(command.aliases) - 1:
                            alias = alias + '`' + command.aliases[i] + '`'
                        else:
                            alias = alias + '`' + command.aliases[i] + '`' + ', '

                # builds and sends embed for command help
                embed=discord.Embed(title=f'{command.name}', description=f'**Description:** {command.description}\n**Usage:**  `{prefix}{command.usage}\n**Aliases:** `{alias}', color=0xc1c100)
                await self.context.send(embed=embed)
            else:
                await self.context.send(embed=embed.make_error_embed("Command not found")) # command is disabled
        except:
            await self.context.send(embed=embed.make_error_embed("Command not found")) # error somehow in getting command

    async def send_bot_help(self, mapping):
        # get list of commands
        cmds = []
        config = configloader.configLoad('guildconfig.json')
        prefix = config.guildPrefix(str(self.context.guild.id))

        for cog, cog_commands in mapping.items():
            cmds = cmds + cog_commands

        newCmds = []
        for item in cmds:
            newCmds.append(str(item))
        newCmds = sorted(newCmds)

        finalCmds = []
        for item in newCmds:
            try:
                randomVar = config[str(self.context.guild.id)]["Commands"][item]
                if randomVar == True:
                    finalCmds.append(item)
            except:
                pass

        cmdString = ""
        if len(finalCmds) != 0:
            for i in range(len(finalCmds)):
                if i == len(finalCmds)-1:
                    cmdString = cmdString + '`' + finalCmds[i] + '`'
                else:
                    cmdString = cmdString + '`' + finalCmds[i] + '`' + ', '

        if cmdString != "":
            embed=discord.Embed(title='Help', description=f'Specify a command to get further information `{prefix}help <command>`', color=0xc1c100)
            embed.add_field(name='Commands', value=f'{cmdString}', inline=False)
        else:
            embed=discord.Embed(title='Help', description=f'No commands found', color=0xc1c100)
        await self.context.send(embed=embed)

def setup(bot):
    bot.add_cog(SetupHelp(bot))