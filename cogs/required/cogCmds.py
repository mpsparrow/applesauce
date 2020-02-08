'''
Commands to manage the loading and enabling of cogs
'''
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
from utils import config, logger
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
            logger.normRun(f'Successfully reloaded {extension}')
            await ctx.message.add_reaction("✅")
        except Exception as e:
            logger.errorRun(f'Failed to reload {extension}')
            logger.errorRun(f'{e}')
            await ctx.message.add_reaction("❌")

    # unload extension
    @commands.command()
    @commands.is_owner()
    async def unloadCog(self, ctx, extension):
        try:
            self.bot.unload_extension(f'cogs.main.{extension}')
            logger.normRun(f'Successfully unloaded {extension}')
            await ctx.message.add_reaction("✅")
        except Exception as e:
            logger.errorRun(f'Failed to unload {extension}')
            logger.errorRun(f'{e}')
            await ctx.message.add_reaction("❌")

    # unload extension
    @commands.command()
    @commands.is_owner()
    async def loadCog(self, ctx, extension):
        try:
            self.bot.load_extension(f'cogs.main.{extension}')
            logger.normRun(f'Successfully loaded {extension}')
            await ctx.message.add_reaction("✅")
        except Exception as e:
            logger.errorRun(f'Failed to load {extension}')
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
                conf = config.readJSON('config.json')
                x = conf['cogs'][extension]
                conf['cogs'][extension] = True
                config.dumpJSON('config.json', conf)
                logger.normRun(f'Successfully enabled {extension}')
                await ctx.message.add_reaction("✅")
            except Exception as e:
                logger.errorRun(f'Failed enabling {extension}')
                logger.errorRun(f'{e}')
                await ctx.message.add_reaction("❌")
        else:
            logger.errorRun(f'Failed enabling {extension}')
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
                conf = config.readJSON('config.json')
                conf['cogs'][extension] = False
                config.dumpJSON('config.json', conf)
                logger.normRun(f'Successfully disabled {extension}')
                await ctx.message.add_reaction("✅")
            except Exception as e:
                logger.errorRun(f'Failed disabling {extension}')
                logger.errorRun(f'{e}')
                await ctx.message.add_reaction("❌")
        else:
            logger.errorRun(f'Failed disabling {extension}')
            await ctx.message.add_reaction("❌")

def setup(bot):
    bot.add_cog(cogCmds(bot))