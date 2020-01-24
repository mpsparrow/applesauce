'''
Custom help command
'''
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
from utils import config, embed

def commandList(cmds):
    cmdString = ""
    if len(cmds) != 0:
        for i in range(len(cmds)):
            cmdString = cmdString + '`' + cmds[i] + '`' + ', '
        cmdString = cmdString[:-2]
        return cmdString
    else:
        return "None"

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
        conf = config.configLoad('guildconfig.json')
        prefix = config.guildPrefix(str(self.context.guild.id))
            
        try:
            randomVar = conf[str(self.context.guild.id)]["Commands"][str(group.name)] # gets true/false value of command for guild
            if randomVar == True: # if command is enabled in guild
                subcmds = ""
                if group.commands != []:
                    for command in group.commands:
                        try:
                            name = f"{group.name} {command.name}"
                            randomVar2 = conf[str(self.context.guild.id)]["Commands"][name]
                            if randomVar2 == True:
                                subcmds = subcmds + '`' + command.name + '`' + ', '
                        except:
                            pass
                    if subcmds != "":
                        subcmds = subcmds[:-2]
                    else:
                        subcmds = "None"
                else:
                    subcmds = "None"

                alias = commandList(group.aliases)

                await self.context.send(embed=embed.make_embed_fields_ninl(group.name, group.description, ("Usage", f"`{prefix}{group.usage}`"), ("Aliases", alias), ("Subcommands", subcmds)))
            else:
                await self.context.send(embed=embed.make_error_embed("Command not found."))
        except:
            await self.context.send(embed=embed.make_error_embed("Command not found."))

    async def send_command_help(self, command):
        conf = config.configLoad('guildconfig.json')
        prefix = config.guildPrefix(str(self.context.guild.id))

        try:
            if command.parent == None:
                name = f"{command.name}"
            else:
                name = f"{command.parent} {command.name}"

            randomVar = conf[str(self.context.guild.id)]["Commands"][str(name)] # gets true/false value of command for guild
            if randomVar == True: # if command is enabled in guild
                alias = commandList(command.aliases)

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

        for command in set(self.context.bot.walk_commands()):
            allCmds.append(str(command))

        allCmds = sorted(allCmds)

        enableCmds = []
        disableCmds= []
        otherCmds = []
        for item in allCmds:
            try:
                randomVar = conf[str(self.context.guild.id)]["Commands"][item]
                if randomVar == True:
                    enableCmds.append(item)
                else:
                    disableCmds.append(item)
            except:
                otherCmds.append(item)
                pass

        enableString = commandList(enableCmds)
        disableString = commandList(disableCmds)
        otherString = commandList(otherCmds)

        if (enableString == "") and (disableString == "") and (otherString == ""):
            embed=discord.Embed(title='Help', description=f'No commands found.', color=0xc1c100)
        else:
            embed=discord.Embed(title='Help', description=f'Specify a command to get further information `{prefix}help <command>`', color=0xc1c100)
            embed.add_field(name='Enabled Commands', value=f'{enableString}', inline=False)
            embed.add_field(name='Disabled Commands', value=f'{disableString}', inline=False)
            embed.add_field(name='Other Commands', value=f'{otherString}', inline=False)
        await self.context.send(embed=embed)

def setup(bot):
    bot.add_cog(SetupHelp(bot))