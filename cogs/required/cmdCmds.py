import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
from logs import logger
from cogs.utils import configloader
import json

class cogCmds(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # disabled command
    @commands.command()
    @commands.is_owner()
    async def disableCmd(self, ctx, cmd):
        try:
            config = configloader.configLoad('guildconfig.json')
            config[str(ctx.guild.id)]["Commands"][cmd] = False
            configloader.configDump('guildconfig.json', config)
            logger.outputWrite(f'Successfully disabled {cmd}')
            await ctx.send(f'Successfully disabled {cmd}')
        except:
            logger.outputWrite(f'Failed to disable {cmd}')
            await ctx.send(f'Failed to disable {cmd}')

    # enable command
    @commands.command()
    @commands.is_owner()
    async def enableCmd(self, ctx, cmd):
        try:
            config = configloader.configLoad('guildconfig.json')
            config[str(ctx.guild.id)]["Commands"][cmd] = True
            configloader.configDump('guildconfig.json', config)
            logger.outputWrite(f'Successfully enabled {cmd}')
            await ctx.send(f'Successfully enabled {cmd}')
        except:
            logger.outputWrite(f'Failed to enable {cmd}')
            await ctx.send(f'Failed to enable {cmd}')

def setup(bot):
    bot.add_cog(cogCmds(bot))