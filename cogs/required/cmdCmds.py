'''
Commands to manage the enabling of individual commands
'''
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
from utils import config, logger
import json

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
                conf = config.readJSON('guildconfig.json')
                conf[str(ctx.guild.id)]["Commands"][str(cmd)] = False
                config.dumpJSON('guildconfig.json', conf)
                logger.normRun(f'Successfully disabled {cmd}')
                await ctx.message.add_reaction("✅")
            else:
                await ctx.message.add_reaction("❌")
        except Exception as e:
            logger.errorRun(f'Failed to disable {cmd}')
            logger.errorRun(f'{e}')
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
                conf = config.readJSON('guildconfig.json')
                conf[str(ctx.guild.id)]["Commands"][str(cmd)] = True
                config.dumpJSON('guildconfig.json', conf)
                logger.normRun(f'Successfully enabled {cmd}')
                await ctx.message.add_reaction("✅")
            else:
                await ctx.message.add_reaction("❌")
        except Exception as e:
            logger.errorRun(f'Failed to enable {cmd}')
            logger.errorRun(f'{e}')
            await ctx.message.add_reaction("❌")

    # enable command
    @commands.command()
    @commands.is_owner()
    async def removeCmd(self, ctx, *, cmd):
        allCmd = []
        for command in set(ctx.bot.walk_commands()):
            allCmd.append(str(command))
        try:
            if str(cmd) in allCmd:
                conf = config.readJSON('guildconfig.json')
                del conf[str(ctx.guild.id)]["Commands"][str(cmd)]
                config.dumpJSON('guildconfig.json', conf)
                logger.normRun(f'Successfully removed {cmd}')
                await ctx.message.add_reaction("✅")
            else:
                await ctx.message.add_reaction("❌")
        except Exception as e:
            logger.errorRun(f'Failed to remove {cmd}')
            logger.errorRun(f'{e}')
            await ctx.message.add_reaction("❌")

def setup(bot):
    bot.add_cog(cogCmds(bot))