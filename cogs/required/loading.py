import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
from logs import logger
from cogs.utils import configloader
import json

class Loading(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # commands
    # restart extension
    @commands.command()
    @commands.is_owner()
    async def reload(self, ctx, extension):
        try:
            self.bot.reload_extension(f'cogs.main.{extension}')
            logger.outputWrite(f'Successfully reloaded {extension}')
            await ctx.send(f'Successfully reloaded {extension}')
        except:
            logger.outputWrite(f'Failed to reload {extension}')
            await ctx.send(f'Failed to reloaded {extension}')

    # unload extension
    @commands.command()
    @commands.is_owner()
    async def unload(self, ctx, extension):
        try:
            self.bot.unload_extension(f'cogs.main.{extension}')
            logger.outputWrite(f'Successfully unloaded {extension}')
            await ctx.send(f'Successfully unloaded {extension}')
        except:
            logger.outputWrite(f'Failed to unload {extension}')
            await ctx.send(f'Failed to unloaded {extension}')

    # unload extension
    @commands.command()
    @commands.is_owner()
    async def load(self, ctx, extension):
        try:
            self.bot.load_extension(f'cogs.main.{extension}')
            logger.outputWrite(f'Successfully loaded {extension}')
            await ctx.send(f'Successfully loaded {extension}')
        except:
            logger.outputWrite(f'Failed to load {extension}')
            await ctx.send(f'Failed to load {extension}')

    # enable extension
    @commands.command()
    @commands.is_owner()
    async def enable(self, ctx, extension):
        try:
            with open(r'config.json', 'r') as file:
                json_data = json.load(file)
                json_data['cogs'][extension] = True
            with open(r'config.json', 'w') as file:
                json.dump(json_data, file, indent=2)
            logger.outputWrite(f'Successfully enabled {extension}')
            await ctx.send(f'Successfully enabled {extension}')
        except Exception as e:
            logger.outputWrite(f'  Error: {e}') # output-log.txt
            logger.outputWrite(f'Failed enabling {extension}')
            await ctx.send(f'Failed enabling {extension}')

    # disable extension
    @commands.command()
    @commands.is_owner()
    async def disable(self, ctx, extension):
        try:
            with open(r'config.json', 'r') as file:
                json_data = json.load(file)
                json_data['cogs'][extension] = False
            with open(r'config.json', 'w') as file:
                json.dump(json_data, file, indent=2)
            logger.outputWrite(f'Successfully disabled {extension}')
            await ctx.send(f'Successfully disabled {extension}')
        except:
            logger.outputWrite(f'Failed disabling {extension}')
            await ctx.send(f'Failed disabling {extension}')

def setup(bot):
    bot.add_cog(Loading(bot))
