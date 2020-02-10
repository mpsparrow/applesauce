'''
Custom help command
'''
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
from utils import embed, dbQuery

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

    @commands.command()
    @commands.is_owner()
    async def helpAll(self, ctx):
        allCmds = []
        prefix = dbQuery.prefix(ctx.guild.id)

        for command in set(ctx.bot.walk_commands()):
            allCmds.append(str(command))

        allCmds = sorted(allCmds)

        enableCmds = []
        enableSubCmds = []
        otherCmds = []
        for item in allCmds:
            try:
                randomVar = dbQuery.command(ctx.guild.id, item)
                if randomVar == True:
                    if " " in item:
                        enableSubCmds.append(item)
                    else:
                        enableCmds.append(item)
                elif randomVar == False:
                    otherCmds.append(item)
            except:
                otherCmds.append(item)
                pass

        enableString = commandList(enableCmds)
        enableSubString = commandList(enableSubCmds)
        otherString = commandList(otherCmds)

        if (enableString == "") and (enableSubString == "") and (otherString == ""):
            embed=discord.Embed(title='Help', description=f'No commands found.', color=0xc1c100)
        else:
            embed=discord.Embed(title='Help', description=f'Specify a command to get further information `{prefix}help <command>`', color=0xc1c100)
            embed.add_field(name='Enabled Commands', value=f'{enableString}', inline=False)
            embed.add_field(name='Enabled Sub Commands', value=f'{enableSubString}', inline=False)
            embed.add_field(name='Disabled/Other Commands', value=f'{otherString}', inline=False)
        await ctx.send(embed=embed)

class Help(commands.MinimalHelpCommand):
    async def command_not_found(self, string):
        await self.context.send(embed=embed.make_error_embed("Command not found"))

    async def subcommand_not_found(self, command, string):
        await self.context.send(embed=embed.make_error_embed("Command not found"))

    async def send_cog_help(self, cog):
        await self.context.send(embed=embed.make_error_embed("Command not found"))

    async def send_group_help(self, group):
        prefix = dbQuery.prefix(self.context.guild.id)

        try:
            await group.can_run(self.context)
        except:
            await self.context.send(embed=embed.make_error_embed("Command not found"))
            return
            
        try:
            randomVar = dbQuery.command(self.context.guild.id, group.name) # gets true/false value of command for guild
            if randomVar == True: # if command is enabled in guild
                subcmds = ""
                if group.commands != []:
                    for command in group.commands:
                        try:
                            name = f"{group.name} {command.name}"
                            randomVar2 = dbQuery.command(self.context.guild.id, name)
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
        prefix = dbQuery.prefix(self.context.guild.id)

        try:
            await command.can_run(self.context)
        except:
            await self.context.send(embed=embed.make_error_embed("Command not found"))
            return

        try:
            if command.parent == None:
                name = f"{command.name}"
                randomVar2 = True
            else:
                name = f"{command.parent} {command.name}"
                randomVar2 = dbQuery.command(self.context.guild.id, command.parent)

            randomVar = dbQuery.command(self.context.guild.id, name) # gets true/false value of command for guild
            if randomVar and randomVar2: # if command is enabled in guild
                alias = commandList(command.aliases)

                await self.context.send(embed=embed.make_embed_fields_ninl(command.name, command.description, ("Usage", f"`{prefix}{command.usage}`"), ("Aliases", alias)))
            else:
                await self.context.send(embed=embed.make_error_embed("Command not found"))
        except:
            await self.context.send(embed=embed.make_error_embed("Command not found"))

    async def send_bot_help(self, mapping):
        # get list of commands
        allCmds = []
        prefix = dbQuery.prefix(self.context.guild.id)

        for command in set(self.context.bot.walk_commands()):
            try:
                await command.can_run(self.context)
                allCmds.append(str(command))
            except:
                pass

        allCmds = sorted(allCmds)
        enableCmds = []
        for item in allCmds:
            try:
                randomVar = dbQuery.command(self.context.guild.id, item)
                if (randomVar == True) and (" " not in item):
                    enableCmds.append(item)
            except:
                pass

        enableString = commandList(enableCmds)
        embed=discord.Embed(title='Help', description=f'Specify a command to get further information `{prefix}help <command>`', color=0xc1c100)
        embed.add_field(name='Commands', value=f'{enableString}', inline=False)
        await self.context.send(embed=embed)

def setup(bot):
    bot.add_cog(SetupHelp(bot))