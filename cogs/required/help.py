'''
Custom help command
'''
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
from utils import config, embed

class SetupHelp(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._original_help_command = bot.help_command
        bot.help_command = Help()
        bot.help_command.cog = self
        
    def cog_unload(self):
        self.bot.help_command = self._original_help_command

class Help(commands.MinimalHelpCommand):
    async def command_not_found(self, string):
        await self.context.send(embed=embed.make_error_embed("Command not found"))

    async def subcommand_not_found(self, command, string):
        await self.context.send(embed=embed.make_error_embed("Command not found"))

    async def send_cog_help(self, cog):
        await self.context.send(embed=embed.make_error_embed("Command not found"))

    async def send_group_help(self, group):
        conf = config.configLoad('guildconfig.json') # loads guildconfig.json
        try:
            prefix = conf[str(self.context.guild.id)]['prefix']
        except:
            conf2 = config.configLoad('config.json')
            prefix = conf2['main']['prefix']
            
        try:
            subcmds = ""
            if group.commands != []:
                for command in group.commands:
                    subcmds += "`" + command.name + "`, "
                subcmds = subcmds[:-2]
            else:
                subcmds = "`None`"

            alias = ""
            if group.aliases != []:
                for i in range(len(group.aliases)):
                    if i == len(group.aliases) - 1:
                        alias = alias + '`' + group.aliases[i] + '`'
                    else:
                        alias = alias + '`' + group.aliases[i] + '`' + ', '
            else:
                alias = "`None`"

            await self.context.send(embed=embed.make_embed_fields_ninl(group.name, group.description, ("Usage", f"`{prefix}{group.usage}`"), ("Aliases", alias), ("Subcommands", subcmds)))
        except:
            await self.context.send(embed=embed.make_error_embed("Command not found"))

    async def send_command_help(self, command):
        conf = config.configLoad('guildconfig.json') # loads guildconfig.json
        try:
            prefix = conf[str(self.context.guild.id)]['prefix']
        except:
            conf2 = config.configLoad('config.json')
            prefix = conf2['main']['prefix']

        try:
            randomVar = conf[str(self.context.guild.id)]["Commands"][str(command.name)] # gets true/false value of command for guild
            if randomVar == True: # if command is enabled in guild
                # creates list of aliases for command
                alias = ''
                if command.aliases != []:
                    for i in range(len(command.aliases)):
                        if i == len(command.aliases) - 1:
                            alias = alias + '`' + command.aliases[i] + '`'
                        else:
                            alias = alias + '`' + command.aliases[i] + '`' + ', '
                else:
                    alias = 'None'

                await self.context.send(embed=embed.make_embed_fields_ninl(command.name, command.description, ("Usage", f"`{prefix}{command.usage}`"), ("Aliases", alias)))
            else:
                await self.context.send(embed=embed.make_error_embed("Command not found"))
        except:
            await self.context.send(embed=embed.make_error_embed("Command not found"))

    async def send_bot_help(self, mapping):
        # get list of commands
        allCmds = []
        conf = config.configLoad('guildconfig.json')
        prefix = config.guildPrefix(str(self.context.guild.id))

        for cog, cmds in mapping.items():
            allCmds += cmds

        newCmds = []
        for item in allCmds:
            newCmds.append(str(item))
        newCmds = sorted(newCmds)

        finalCmds = []
        for item in newCmds:
            try:
                randomVar = conf[str(self.context.guild.id)]["Commands"][item]
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
            embed=discord.Embed(title='Help', description=f'No commands found.', color=0xc1c100)
        await self.context.send(embed=embed)

def setup(bot):
    bot.add_cog(SetupHelp(bot))