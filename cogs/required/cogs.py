'''
Commands to manage the loading and enabling of cogs
'''
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
from utils import logger, dbConnect
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
            logger.normRun(f'Successfully reloaded cog: {extension}')
            await ctx.message.add_reaction("✅")
        except Exception as e:
            logger.errorRun(f'Failed to reload cog: {extension}')
            logger.errorRun(f'{e}')
            await ctx.message.add_reaction("❌")

    # unload extension
    @commands.command()
    @commands.is_owner()
    async def unloadCog(self, ctx, extension):
        try:
            self.bot.unload_extension(f'cogs.main.{extension}')
            logger.normRun(f'Successfully unloaded cog: {extension}')
            await ctx.message.add_reaction("✅")
        except Exception as e:
            logger.errorRun(f'Failed to unload cog: {extension}')
            logger.errorRun(f'{e}')
            await ctx.message.add_reaction("❌")

    # unload extension
    @commands.command()
    @commands.is_owner()
    async def loadCog(self, ctx, extension):
        try:
            self.bot.load_extension(f'cogs.main.{extension}')
            logger.normRun(f'Successfully loaded cog: {extension}')
            await ctx.message.add_reaction("✅")
        except Exception as e:
            logger.errorRun(f'Failed to load cog: {extension}')
            logger.errorRun(f'{e}')
            await ctx.message.add_reaction("❌")

    # enable extension
    @commands.command()
    @commands.is_owner()
    async def enableCog(self, ctx, extension):
        flag = False
        try:
            self.bot.load_extension(f'cogs.main.{extension}')
            self.bot.unload_extension(f'cogs.main.{extension}')
            flag = True
        except:
            try:
                self.bot.unload_extension(f'cogs.main.{extension}')
                self.bot.load_extension(f'cogs.main.{extension}')
                flag = True
            except:
                pass

        if flag == True:
            try:
                dbConnect.cogs(extension, True)
                logger.normRun(f'Successfully enabled cog: {extension}')
                await ctx.message.add_reaction("✅")
            except Exception as e:
                logger.errorRun(f'Failed to enable cog: {extension}')
                logger.errorRun(f'{e}')
                await ctx.message.add_reaction("❌")
        else:
            logger.errorRun(f'Failed to enable cog: {extension}')
            await ctx.message.add_reaction("❌")

    # disable extension
    @commands.command()
    @commands.is_owner()
    async def disableCog(self, ctx, extension):
        flag = False
        try:
            self.bot.load_extension(f'cogs.main.{extension}')
            self.bot.unload_extension(f'cogs.main.{extension}')
            flag = True
        except:
            try:
                self.bot.unload_extension(f'cogs.main.{extension}')
                self.bot.load_extension(f'cogs.main.{extension}')
                flag = True
            except:
                pass
            
        if flag == True:
            try:
                dbConnect.cogs(extension, False)
                logger.normRun(f'Successfully disabled cog: {extension}')
                await ctx.message.add_reaction("✅")
            except Exception as e:
                logger.errorRun(f'Failed to disable cog: {extension}')
                logger.errorRun(f'{e}')
                await ctx.message.add_reaction("❌")
        else:
            logger.errorRun(f'Failed to disable cog: {extension}')
            await ctx.message.add_reaction("❌")

def setup(bot):
    bot.add_cog(cogCmds(bot))