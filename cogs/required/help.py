import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
from util import embed as emb
from util.db.query import queryPrefix

class Help(commands.Cog):
    """
    Cog for help command.
    """

    def __init__(self, bot):
        self._original_help_command = bot.help_command
        bot.help_command = SetupHelp()
        bot.help_command.cog = self


class SetupHelp(commands.MinimalHelpCommand):
    """
    Main help command.
    """
    async def command_not_found(self, string):
        await self.context.send(embed=emb.make_error("Command not found."))

    async def subcommand_not_found(self, command, string):
        await self.context.send(embed=emb.make_error("Sub-command not found."))

    async def send_cog_help(self, cog):
        await self.context.send("Cog help")

    async def send_group_help(self, group):
        await self.context.send("Group help")
        
    async def send_command_help(self, command):
        await self.context.send("command help")

    async def send_bot_help(self, mapping):
        cmds = []
        for cmd in self.context.bot.walk_commands():
            print(cmd)
            if not(cmd.hidden):
                cmds.append(cmd)

        cmdString = ""
        for cmd in set(cmds):
            if not(' ' in cmd):
                cmdString += f"`{cmd}`, "

        embed = emb.make("Help", f"Specify a command/cog to get further information `{queryPrefix.prefix(self.context.guild.id)}help <command>`")
        embed.add_field(name="Commands", value=cmdString[:-2], inline=False)
        await self.context.send(embed=embed)

def setup(bot):
    bot.add_cog(Help(bot))