'''
Owner level cog management.
'''
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
from util import runLog, dbInsert

        
class cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="cog", description="Controlling cogs at owner level.", usage="cog <action> <cog name>", aliases=["c"])
    @commands.is_owner()
    async def cog(self, ctx):
        pass


    @cog.command(name="enable", description="Enable loading of cog on bot startup.", usage="cog enable <cog name>", aliases=["e"])
    async def enable(self, ctx, extension):
        try:
            db # update status
        except CogStateError:
            # The cog state was unable to be changed.
            runLog.error(f"Cog '{extension}' failed to change startup state. CogStateError (cog.enable)")
            await ctx.message.add_reaction("❌")
        else:
            runLog.log(f"Cog '{extension}' enabled on startup. (cog.enable)")
            await ctx.message.add_reaction("✅")


    @cog.command(name="disable", description="Disable loading of cog on bot startup.", usage="cog disable <cog name>", aliases=["d"])
    async def disable(self, ctx, extension):
        try:
            db # update status
        except CogStateError:
            # The cog state was unable to be changed.
            runLog.error(f"Cog '{extension}' failed to change startup state. CogStateError (cog.disable)")
            await ctx.message.add_reaction("❌")
        else:
            runLog.log(f"Cog '{extension}' disabled on startup. (cog.disable)")
            await ctx.message.add_reaction("✅")


    @cog.command(name="load", description="Load cog while bot is running.", usage="cog load <cog name>", aliases=["l"])
    async def load(self, ctx, extension):
        try:
            # Attempt to load cog.
            self.bot.load_extension(f'cogs.main.{extension}')
        except ExtensionNotFound:
            # The cog could not be found.
            runLog.error(f"Cog '{extension}' was not found. ExtensionNotFound (cog.load)")
            await ctx.message.add_reaction("❌")
        except ExtensionAlreadyLoaded:
            # The cog was already loaded.
            runLog.warn(f"Cog '{extension}' was already loaded. ExtensionAlreadyLoaded (cog.load)")
            await ctx.message.add_reaction("✅")
        except NoEntryPointError:
            # The cog does not have a setup function.
            runLog.error(f"Cog '{extension}' has no setup function. NoEntryPointError (cog.load)")
            dbInsert.cogs(extension, False) # Set cog state to not loaded in database.
            await ctx.message.add_reaction("⚠️")
        except ExtensionFailed:
            # The cog setup function has an execution error.
            runLog.error(f"Cog '{extension}' has an execution error. ExtensionFailed (cog.load)")
            dbInsert.cogs(extension, False) # Set cog state to not loaded in database.
            await ctx.message.add_reaction("⚠️")
        else:
            runLog.log(f"Cog '{extension}' loaded. (cog.load)")
            dbInsert.cogs(extension, True) # Set cog state to loaded in database.
            await ctx.message.add_reaction("✅")


    @cog.command(name="unload", description="Unload cog while bot is running.", usage="cog unload <cog name>", aliases=["u"])
    async def unload(self, ctx, extension):
        try:
            # Attempt to unload cog.
            self.bot.unload_extension(f'cogs.main.{extension}')
        except ExtensionNotLoaded:
            # The cog was not found or unloaded.
            runLog.error(f"Cog '{extension}' was unable to be unloaded and/or found. ExtensionNotLoaded (cog.unload)")
            await ctx.message.add_reaction("❌")
        else:
            runLog.log(f"Cog '{extension}' unloaded. (cog.unload)")
            dbInsert.cogs(extension, False) # Set cog state to not loaded in database.
            await ctx.message.add_reaction("✅")   


    @cog.command(name="reload", description="Reload cog while bot is running.", usage="cog reload <cog name>", aliases=["r"])
    async def reload(self, ctx, extension):
        try:
            # Attempt to reload cog.
            self.bot.reload_extension(f'cogs.main.{extension}')
        except ExtensionNotLoaded:
            # The cog was not reloaded.
            runLog.error(f"Cog '{extension}' was unable to be reloaded. ExtensionNotLoaded (cog.reload)")
            dbInsert.cogs(extension, False) # Set cog state to not loaded in database.
            await ctx.message.add_reaction("⚠️")
        except ExtensionNotFound:
            # The cog could not be found.
            runLog.warn(f"Cog '{extension}' was not found. ExtensionNotFound (cog.reload)")
            await ctx.message.add_reaction("❌")
        except NoEntryPointError:
            # The cog does not have a setup function.
            runLog.error(f"Cog '{extension}' has no setup function. NoEntryPointError (cog.reload)")
            dbInsert.cogs(extension, False) # Set cog state to not loaded in database.
            await ctx.message.add_reaction("⚠️")
        except ExtensionFailed:
            # The cog setup function has an execution error.
            runLog.error(f"Cog '{extension}' has an execution error. ExtensionFailed (cog.reload)")
            dbInsert.cogs(extension, False) # Set cog state to not loaded in database.
            await ctx.message.add_reaction("⚠️")
        else:
            runLog.info(f"Cog '{extension}' reloaded. (cog.reload)")
            dbInsert.cogs(extension, True) # Set cog state to loaded in database.
            await ctx.message.add_reaction("✅")           

def setup(bot):
    bot.add_cog(cog(bot))