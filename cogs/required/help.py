import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
from cogs.utils import configloader

class SetupHelp(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._original_help_command = bot.help_command
        bot.help_command = Help()
        bot.help_command.cog = self

class Help(commands.MinimalHelpCommand):
    async def command_not_found(self, string):
        await self.context.send("command unavailable")

    async def subcommand_not_found(self, command, string):
        await self.context.send("command unavailable")

    async def send_cog_help(self, cog):
        await self.context.send("command unavailable")

    async def send_group_help(self, group):
        await self.context.send("command unavailable")

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
                alias = f'\n**Aliases:** '
                if command.aliases == []:
                    alias = ""
                else:
                    for i in range(len(command.aliases)):
                        if i == len(command.aliases) - 1:
                            alias = alias + '`' + command.aliases[i] + '`'
                        else:
                            alias = alias + '`' + command.aliases[i] + '`' + ', '

                # builds and sends embed for command help
                embed=discord.Embed(title=f'Help - {command.name}', description=f'**Description:** {command.description}\n**Usage:**  `{prefix}{command.usage}`{alias}', color=0xc1c100)
                await self.context.send(embed=embed)
            else:
                await self.context.send("command unavailable") # command is disabled
        except:
            await self.context.send("command unavailable") # error somehow in getting command

    async def send_bot_help(self, mapping):
        # get list of commands
        cmds = []
        config = configloader.configLoad('guildconfig.json') # loads guildconfig.json

        try:
            prefix = config[str(self.context.guild.id)]['prefix']
        except:
            config2 = configloader.configLoad('config.json')
            prefix = config2['main']['prefix']

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
        if len(finalCmds) == 0:
            cmdString = "no commands found"
        else:
            for i in range(len(finalCmds)):
                if i == len(finalCmds)-1:
                    cmdString = cmdString + '`' + finalCmds[i] + '`'
                else:
                    cmdString = cmdString + '`' + finalCmds[i] + '`' + ', '

        # add all commands to embed and message it
        embed=discord.Embed(title='Help', description=f'Specify a command to see more information (i.e. `{prefix}help 8ball`). Use prefix `{prefix}` for all commands. ', color=0xc1c100)
        embed.add_field(name='Commands', value=f'{cmdString}', inline=False)
        await self.context.send(embed=embed)

def setup(bot):
    bot.add_cog(SetupHelp(bot))