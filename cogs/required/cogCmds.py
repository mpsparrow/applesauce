import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
from cogs.utils import configloader, logger
import json

class cogCmds(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # commands
    # restart extension
    @commands.command()
    @commands.is_owner()
    async def reloadCog(self, ctx, extension):
        try:
            self.bot.reload_extension(f'cogs.main.{extension}')
            logger.logWrite('output-log.txt', f'Successfully reloaded {extension}')
            await ctx.send(f'Successfully reloaded {extension}')
        except:
            logger.logWrite('output-log.txt', f'Failed to reload {extension}')
            await ctx.send(f'Failed to reload {extension}')

    # unload extension
    @commands.command()
    @commands.is_owner()
    async def unloadCog(self, ctx, extension):
        try:
            self.bot.unload_extension(f'cogs.main.{extension}')
            logger.logWrite('output-log.txt', f'Successfully unloaded {extension}')
            await ctx.send(f'Successfully unloaded {extension}')
        except:
            logger.logWrite('output-log.txt', f'Failed to unload {extension}')
            await ctx.send(f'Failed to unload {extension}')

    # unload extension
    @commands.command()
    @commands.is_owner()
    async def loadCog(self, ctx, extension):
        try:
            self.bot.load_extension(f'cogs.main.{extension}')
            logger.logWrite('output-log.txt', f'Successfully loaded {extension}')
            await ctx.send(f'Successfully loaded {extension}')
        except:
            logger.logWrite('output-log.txt', f'Failed to load {extension}')
            await ctx.send(f'Failed to load {extension}')

    # enable extension
    @commands.command()
    @commands.is_owner()
    async def enableCog(self, ctx, extension):
        try:
            config = configloader.configLoad('config.json')
            config['cogs'][extension] = True
            configloader.configDump('config.json', config)
            logger.logWrite('output-log.txt', f'Successfully enabled {extension}')
            await ctx.send(f'Successfully enabled {extension}')
        except Exception as e:
            logger.logWrite('output-log.txt', f'  Error: {e}') # output-log.txt
            logger.logWrite('output-log.txt', f'Failed enabling {extension}')
            await ctx.send(f'Failed enabling {extension}')

    # disable extension
    @commands.command()
    @commands.is_owner()
    async def disableCog(self, ctx, extension):
        try:
            config = configloader.configLoad('config.json')
            config['cogs'][extension] = False
            configloader.configDump('config.json', config)
            logger.logWrite('output-log.txt', f'Successfully disabled {extension}')
            await ctx.send(f'Successfully disabled {extension}')
        except:
            logger.logWrite('output-log.txt', f'Failed disabling {extension}')
            await ctx.send(f'Failed disabling {extension}')

def setup(bot):
    bot.add_cog(cogCmds(bot))