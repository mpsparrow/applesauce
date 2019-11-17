import discord
from discord.ext import commands
from logs import logger

class Error(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # logs command errors
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound): # invalid command, command not found
            logger.commandWrite(f'{ctx.message.author} invalid command {ctx.message.content}')

        if isinstance(error, commands.MissingRole): # invalid permissions, missing role
            logger.commandWrite(f'{ctx.message.author} no permission {ctx.message.content}')

    # logs every command used
    @commands.Cog.listener()
    async def on_command(self, ctx):
        logger.commandWrite(f'{ctx.message.author} used {ctx.message.content}')


def setup(bot):
    bot.add_cog(Error(bot))
