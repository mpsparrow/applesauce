import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
from util.log import runLog
from util.insert import insertCog

class cogManage(commands.Cog, name="Cog Management"):
    """
    Cog containing main owner commands for controlling cogs.
    """
    
    def __init__(self, bot):
        """
        Constructor
        :param bot:
        """
        self.bot = bot

    ## Group for cog management commands.
    @commands.group(name="cog", description="Controlling cogs at owner level.", usage="cog <action> <cog name>", aliases=["c"])
    @commands.is_owner()
    async def cog(self, ctx):
        """
        Command group for cog management.
        :param ctx:
        """
        pass

    ## Enable loading of cog on bot startup.
    @cog.command(name="enable", description="Enable loading of cog on bot startup.", usage="cog enable <cog name>", aliases=["e"])
    async def enable(self, ctx, name):
        """
        Enable loading of cog on bot startup by setting value in DB to True.
        :param ctx:
        :param str name: Cog name
        """
        try:
            insertCog.enabled(name, True) # update status
        except CogStateError:
            # The cog state was unable to be changed.
            runLog.error(f"Cog '{name}' failed to change startup state. CogStateError (cog.enable)")
            await ctx.message.add_reaction("❌")
        else:
            runLog.log(f"Cog '{name}' enabled on startup. (cog.enable)")
            await ctx.message.add_reaction("✅")

    ## Disable loading of cog on bot startup.
    @cog.command(name="disable", description="Disable loading of cog on bot startup.", usage="cog disable <cog name>", aliases=["d"])
    async def disable(self, ctx, name):
        """
        Disable loading of cog on bot startup by setting value in DB to False.
        :param ctx:
        :param str name: Cog name
        """
        try:
            insertCog.enabled(name, False) # update status
        except CogStateError:
            # The cog state was unable to be changed.
            runLog.error(f"Cog '{name}' failed to change startup state. CogStateError (cog.disable)")
            await ctx.message.add_reaction("❌")
        else:
            runLog.log(f"Cog '{name}' disabled on startup. (cog.disable)")
            await ctx.message.add_reaction("✅")

    ## Load cog while bot is running.
    @cog.command(name="load", description="Load cog while bot is running.", usage="cog load <cog name>", aliases=["l"])
    async def load(self, ctx, name):
        """
        Load cog while bot is running.
        `load_extension <https://discordpy.readthedocs.io/en/latest/ext/commands/api.html?highlight=load_extension#discord.ext.commands.Bot.load_extension>`
        :param ctx:
        :param str name: Cog name
        """
        try:
            # Attempt to load cog.
            self.bot.load_extension(f'cogs.main.{name}')
        except ExtensionNotFound:
            # The cog could not be found.
            runLog.error(f"Cog '{name}' was not found. ExtensionNotFound (cog.load)")
            await ctx.message.add_reaction("❌")
        except ExtensionAlreadyLoaded:
            # The cog was already loaded.
            runLog.warn(f"Cog '{name}' was already loaded. ExtensionAlreadyLoaded (cog.load)")
            await ctx.message.add_reaction("✅")
        except NoEntryPointError:
            # The cog does not have a setup function.
            runLog.error(f"Cog '{name}' has no setup function. NoEntryPointError (cog.load)")
            insertCog.disabled(name, False) # Set cog state to not loaded in database.
            await ctx.message.add_reaction("⚠️")
        except ExtensionFailed:
            # The cog setup function has an execution error.
            runLog.error(f"Cog '{name}' has an execution error. ExtensionFailed (cog.load)")
            insertCog.disabled(name, False) # Set cog state to not loaded in database.
            await ctx.message.add_reaction("⚠️")
        else:
            runLog.log(f"Cog '{name}' loaded. (cog.load)")
            insertCog.disabled(name, True) # Set cog state to loaded in database.
            await ctx.message.add_reaction("✅")

    ## Unload cog while bot is running.
    @cog.command(name="unload", description="Unload cog while bot is running.", usage="cog unload <cog name>", aliases=["u"])
    async def unload(self, ctx, name):
        """
        Unload cog while bot is running.
        `unload_extension <https://discordpy.readthedocs.io/en/latest/ext/commands/api.html?highlight=unload_extension#discord.ext.commands.Bot.unload_extension>`
        :param ctx:
        :param str name: Cog name
        """
        try:
            # Attempt to unload cog.
            self.bot.unload_extension(f'cogs.main.{name}')
        except ExtensionNotLoaded:
            # The cog was not found or unloaded.
            runLog.error(f"Cog '{name}' was unable to be unloaded and/or found. ExtensionNotLoaded (cog.unload)")
            await ctx.message.add_reaction("❌")
        else:
            runLog.log(f"Cog '{name}' unloaded. (cog.unload)")
            insertCog.disabled(name, False) # Set cog state to not loaded in database.
            await ctx.message.add_reaction("✅")   

    ## Reload cog while bot is running.
    @cog.command(name="reload", description="Reload cog while bot is running.", usage="cog reload <cog name>", aliases=["r"])
    async def reload(self, ctx, name):
        """
        Reload cog while bot is running.
        `reload_extension <https://discordpy.readthedocs.io/en/latest/ext/commands/api.html?highlight=reload_extension#discord.ext.commands.Bot.reload_extension>`
        :param ctx:
        :param str name: Cog name
        """
        try:
            # Attempt to reload cog.
            self.bot.reload_extension(f'cogs.main.{name}')
        except ExtensionNotLoaded:
            # The cog was not reloaded.
            runLog.error(f"Cog '{name}' was unable to be reloaded. ExtensionNotLoaded (cog.reload)")
            insertCog.disabled(name, False) # Set cog state to not loaded in database.
            await ctx.message.add_reaction("⚠️")
        except ExtensionNotFound:
            # The cog could not be found.
            runLog.warn(f"Cog '{name}' was not found. ExtensionNotFound (cog.reload)")
            await ctx.message.add_reaction("❌")
        except NoEntryPointError:
            # The cog does not have a setup function.
            runLog.error(f"Cog '{name}' has no setup function. NoEntryPointError (cog.reload)")
            insertCog.disabled(name, False) # Set cog state to not loaded in database.
            await ctx.message.add_reaction("⚠️")
        except ExtensionFailed:
            # The cog setup function has an execution error.
            runLog.error(f"Cog '{name}' has an execution error. ExtensionFailed (cog.reload)")
            insertCog.disabled(name, False) # Set cog state to not loaded in database.
            await ctx.message.add_reaction("⚠️")
        else:
            runLog.info(f"Cog '{name}' reloaded. (cog.reload)")
            insertCog.disabled(name, True) # Set cog state to loaded in database.
            await ctx.message.add_reaction("✅")           

## Cog setup function.
def setup(bot):
    bot.add_cog(cogManage(bot))