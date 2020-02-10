'''
Commands to manage the enabling of individual commands
'''
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
from utils import logger, dbConnect

class cogCmds(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # disabled command
    @commands.command()
    @commands.is_owner()
    async def disableCmd(self, ctx, *, cmd):
        allCmd = []
        for command in set(ctx.bot.walk_commands()):
            allCmd.append(str(command))
        try:
            if str(cmd) in allCmd:
                dbConnect.commands(ctx.guild.id, cmd, False)
                logger.normRun(f"Successfully disabled {cmd}")
                await ctx.message.add_reaction("✅")
            else:
                logger.warnRun(f"Commend doesn't exist {cmd}")
                await ctx.message.add_reaction("❌")
        except Exception as e:
            logger.errorRun(f"Failed to disable {cmd}")
            logger.normRun(e)
            await ctx.message.add_reaction("❌")

    # enable command
    @commands.command()
    @commands.is_owner()
    async def enableCmd(self, ctx, *, cmd):
        allCmd = []
        for command in set(ctx.bot.walk_commands()):
            allCmd.append(str(command))
        try:
            if str(cmd) in allCmd:
                dbConnect.commands(ctx.guild.id, cmd, True)
                logger.normRun(f"Successfully enabled {cmd}")
                await ctx.message.add_reaction("✅")
            else:
                logger.warnRun(f"Command doesn't exist {cmd}")
                await ctx.message.add_reaction("❌")
        except Exception as e:
            logger.errorRun(f"Failed to enable {cmd}")
            logger.normRun(e)
            await ctx.message.add_reaction("❌")

def setup(bot):
    bot.add_cog(cogCmds(bot))