import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
from util import embed as emb
from util.db.query import queryPrefix, queryCogGuild

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
        embed = emb.make(command.name, command.help)
        embed.add_field(name="Usage", value=f"{queryPrefix.prefix(self.context.guild.id)}{command.full_parent_name} {command.name}", inline=False)
        embed.add_field(name="Aliases", value=f"{command.aliases}", inline=False)
        # embed.set_footer(text=f"Cog: {command.cog.name}")
        await self.context.send(embed=embed)

    async def send_bot_help(self, mapping):
        embed = emb.make("Help", f"Specify a command/cog to get further information `{queryPrefix.prefix(self.context.guild.id)}help <command>`")

        for x in self.context.bot.cogs:
            cmdString = ""
            if queryCogGuild.status(self.context.guild.id, x):
                for y in set(self.context.bot.walk_commands()):
                    if (y.cog_name == x) and (" " not in str(y)):
                        cmdString += f"`{y}`, "

                if len(cmdString) > 0:
                    embed.add_field(name=x, value=cmdString[:-2], inline=False)

        await self.context.send(embed=embed)

def setup(bot):
    bot.add_cog(Help(bot))