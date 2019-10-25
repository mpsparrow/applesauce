import discord
from discord.ext import commands
from discord.ext.commands import has_permissions

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # commands
    # restart extension
    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def reload(self, ctx, extension):
        try:
            self.bot.reload_extension(f'cogs.{extension}')
            print(f'Successfully reloaded {extension}')
            await ctx.send(f'Successfully reloaded {extension}')
        except:
            print(f'Failed to reload {extension}')
            await ctx.send(f'Failed to reloaded {extension}')

    # unload extension
    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def unload(self, ctx, extension):
        try:
            self.bot.unload_extension(f'cogs.{extension}')
            print(f'Successfully unloaded {extension}')
            await ctx.send(f'Successfully unloaded {extension}')
        except:
            print(f'Failed to unload {extension}')
            await ctx.send(f'Failed to unloaded {extension}')

    # unload extension
    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def load(self, ctx, extension):
        try:
            self.bot.load_extension(f'cogs.{extension}')
            print(f'Successfully loaded {extension}')
            await ctx.send(f'Successfully loaded {extension}')
        except:
            print(f'Failed to load {extension}')
            await ctx.send(f'Failed to load {extension}')

def setup(bot):
    bot.add_cog(Admin(bot))
