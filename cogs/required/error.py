'''
Basic error checking, logging, and ignoring
'''
import discord
from discord.ext import commands
from utils import logger

class Error(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # logs command errors
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound): # invalid command, command not found
            logger.logWrite('command-log.txt', f'{ctx.message.author} invalid command {ctx.message.content}')

        if isinstance(error, commands.MissingRole): # invalid permissions, missing role
            logger.logWrite('command-log.txt', f'{ctx.message.author} no permission {ctx.message.content}')

    # logs every command used
    @commands.Cog.listener()
    async def on_command(self, ctx):
        logger.logWrite('command-log.txt', f'{ctx.message.author} used {ctx.message.content}')

    # ignores all bots in Discord
    @commands.Cog.listener()
    async def on_message(self, ctx):
        if ctx.author == self.bot.user:
            return
            
def setup(bot):
    bot.add_cog(Error(bot))