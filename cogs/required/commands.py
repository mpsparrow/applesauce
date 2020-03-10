# Commands cog
# For enabling and disabling commands per guild
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
from util import logger, dbInsert


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
                dbInsert.commands(ctx.guild.id, cmd, False)
                logger.normRun(f"Successfully disabled command: {cmd}")
                await ctx.message.add_reaction("✅")
            else:
                logger.warnRun(f"Commend doesn't exist: {cmd}")
                await ctx.message.add_reaction("❌")
        except Exception as e:
            logger.errorRun(f"Failed to disable command: {cmd}")
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
                dbInsert.commands(ctx.guild.id, cmd, True)
                logger.normRun(f"Successfully enabled command: {cmd}")
                await ctx.message.add_reaction("✅")
            else:
                logger.warnRun(f"Command doesn't exist: {cmd}")
                await ctx.message.add_reaction("❌")
        except Exception as e:
            logger.errorRun(f"Failed to enable command: {cmd}")
            logger.normRun(e)
            await ctx.message.add_reaction("❌")

def setup(bot):
    bot.add_cog(cogCmds(bot))