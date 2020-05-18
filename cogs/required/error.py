"""
Message and command error checking and logging
"""
import discord
from discord.ext import commands
from util.log import runLog

class Error(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # logs command errors
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound): # invalid command, command not found
            runLog.warn(f"{ctx.message.author} invalid command {ctx.message.content}")
        elif isinstance(error, commands.MissingRole): # invalid permissions, missing role
            runLog.warn(f"{ctx.message.author} no permission {ctx.message.content}")
        else:
            runLog.warn(f"{ctx.message.author} {ctx.message.content} {error}")

    # ignores all bots in Discord
    @commands.Cog.listener()
    async def on_message(self, ctx):
        if ctx.author == self.bot.user:
            return
            
def setup(bot):
    bot.add_cog(Error(bot))
