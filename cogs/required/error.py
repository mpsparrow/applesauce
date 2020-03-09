# Error cog
# Catches and logs commands and command errors
import discord
from discord.ext import commands
from util import logger

class Error(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # logs command errors
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound): # invalid command, command not found
            logger.write('command-log.txt', f'{ctx.message.author} invalid command {ctx.message.content}')
        elif isinstance(error, commands.MissingRole): # invalid permissions, missing role
            logger.write('command-log.txt', f'{ctx.message.author} no permission {ctx.message.content}')
        else:
            logger.write('runtime-log.txt', f'Error: {error}')

    # logs every command used
    @commands.Cog.listener()
    async def on_command(self, ctx):
        logger.write('command-log.txt', f'{ctx.message.author} used {ctx.message.content}')

    # ignores all bots in Discord
    @commands.Cog.listener()
    async def on_message(self, ctx):
        if ctx.author == self.bot.user:
            return
            
def setup(bot):
    bot.add_cog(Error(bot))
