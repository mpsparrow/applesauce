import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
from logs import logger
from cogs.utils import configloader
import json

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # commands
    # change prefix
    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def prefix(self, ctx, prefix):
        with open('config.json', 'r') as file:
            json_data = json.load(file)
            json_data['main']['prefix'] = prefix
        with open('config.json', 'w') as file:
            json.dump(json_data, file, indent=2)
        await ctx.send(f'prefix changed to: {prefix}')

    # restart extension
    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def reload(self, ctx, extension):
        try:
            self.bot.reload_extension(f'cogs.addons.{extension}')
            logger.outputWrite(f'Successfully reloaded {extension}')
            await ctx.send(f'Successfully reloaded {extension}')
        except:
            logger.outputWrite(f'Failed to reload {extension}')
            await ctx.send(f'Failed to reloaded {extension}')

    # unload extension
    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def unload(self, ctx, extension):
        try:
            self.bot.unload_extension(f'cogs.addons.{extension}')
            logger.outputWrite(f'Successfully unloaded {extension}')
            await ctx.send(f'Successfully unloaded {extension}')
        except:
            logger.outputWrite(f'Failed to unload {extension}')
            await ctx.send(f'Failed to unloaded {extension}')

    # unload extension
    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def load(self, ctx, extension):
        try:
            self.bot.load_extension(f'cogs.addons.{extension}')
            logger.outputWrite(f'Successfully loaded {extension}')
            await ctx.send(f'Successfully loaded {extension}')
        except:
            logger.outputWrite(f'Failed to load {extension}')
            await ctx.send(f'Failed to load {extension}')

def setup(bot):
    bot.add_cog(Admin(bot))
