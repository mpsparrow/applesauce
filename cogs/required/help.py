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

def botHelp(ctx, passAll=False):
    # get list of commands
    allCmds = []
    conf = config.configLoad('guildconfig.json')
    prefix = config.guildPrefix(str(ctx.guild.id))

    for command in set(ctx.bot.walk_commands()):
        allCmds.append(str(command))

    allCmds = sorted(allCmds)

    enableCmds = []
    enableSubCmds = []
    disableCmds= []
    otherCmds = []
    for item in allCmds:
        try:
            randomVar = conf[str(ctx.guild.id)]["Commands"][item]
            if randomVar == True:
                if " " in item:
                    enableSubCmds.append(item)
                else:
                    enableCmds.append(item)
            else:
                disableCmds.append(item)
        except:
            otherCmds.append(item)
            pass

    enableString = commandList(enableCmds)
    enableSubString = commandList(enableSubCmds)
    disableString = commandList(disableCmds)
    otherString = commandList(otherCmds)

    if (enableString == "") and (disableString == "") and (otherString == ""):
        embed=discord.Embed(title='Help', description=f'No commands found.', color=0xc1c100)
    else:
        embed=discord.Embed(title='Help', description=f'Specify a command to get further information `{prefix}help <command>`', color=0xc1c100)
        if passAll == True:
            embed.add_field(name='Enabled Commands', value=f'{enableString}', inline=False)
            embed.add_field(name='Enabled Sub Commands', value=f'{enableSubString}', inline=False)
            embed.add_field(name='Disabled Commands', value=f'{disableString}', inline=False)
            embed.add_field(name='Other Commands', value=f'{otherString}', inline=False)
        else:
            embed.add_field(name='Commands', value=f'{enableString}', inline=False)
    return embed

class SetupHelp(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._original_help_command = bot.help_command
        bot.help_command = Help()
        bot.help_command.cog = self

    # disabled command
    @commands.command()
    @commands.is_owner()
    async def helpAll(self, ctx):
        await ctx.send(embed=botHelp(ctx, True))

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
                await self.context.send(embed=embed.make_error_embed("Command not found"))
        except:
            await self.context.send(embed=embed.make_error_embed("Command not found"))

    async def send_command_help(self, command):
        conf = config.configLoad('guildconfig.json')
        prefix = config.guildPrefix(str(self.context.guild.id))

        try:
            if command.parent == None:
                name = f"{command.name}"
                randomVar2 = True
            else:
                name = f"{command.parent} {command.name}"
                randomVar2 = conf[str(self.context.guild.id)]["Commands"][str(command.parent)]

            randomVar = conf[str(self.context.guild.id)]["Commands"][str(name)] # gets true/false value of command for guild
            if randomVar and randomVar2: # if command is enabled in guild
                alias = commandList(command.aliases)

                await self.context.send(embed=embed.make_embed_fields_ninl(command.name, command.description, ("Usage", f"`{prefix}{command.usage}`"), ("Aliases", alias)))
            else:
                await self.context.send(embed=embed.make_error_embed("Command not found"))
        except:
            await self.context.send(embed=embed.make_error_embed("Command not found"))

    async def send_bot_help(self, mapping):
        await self.context.send(embed=botHelp(self.context))

def setup(bot):
    bot.add_cog(SetupHelp(bot))