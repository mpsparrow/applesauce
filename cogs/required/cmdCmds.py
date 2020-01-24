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
                conf = config.configLoad('guildconfig.json')
                conf[str(ctx.guild.id)]["Commands"][str(cmd)] = False
                config.configDump('guildconfig.json', conf)
                logger.normalLog(f'Successfully disabled {cmd}')
                await ctx.message.add_reaction("✅")
            else:
                await ctx.message.add_reaction("❌")
        except Exception as e:
            logger.errorLog(f'Failed to disable {cmd}')
            logger.errorLog(f'{e}')
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
                conf = config.configLoad('guildconfig.json')
                conf[str(ctx.guild.id)]["Commands"][str(cmd)] = True
                config.configDump('guildconfig.json', conf)
                logger.normalLog(f'Successfully enabled {cmd}')
                await ctx.message.add_reaction("✅")
            else:
                await ctx.message.add_reaction("❌")
        except Exception as e:
            logger.errorLog(f'Failed to enable {cmd}')
            logger.errorLog(f'{e}')
            await ctx.message.add_reaction("❌")

def setup(bot):
    bot.add_cog(cogCmds(bot))