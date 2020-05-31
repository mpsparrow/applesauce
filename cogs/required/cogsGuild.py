import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
from util.log import runLog
from util.db.insert import insertCogGuild
from util.db.query import queryCogList

class cogGuild(commands.Cog):
    """
    Cog containing main guild commands for controlling cogs.
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def disableCog(self, ctx, cog):
        """
        Disable the use of the cog in specific guild.
        :param ctx:
        :param str cog: Cog name
        """
        try:
            value = queryCogList.loaded(cog)
            if value:
                insertCogGuild.cog(ctx.guild.id, cog, False)
                runLog.error(f"Disabled cog ({cog}) for guild. (cogsGuild.disableCog)")
                await ctx.message.add_reaction("✅")
            else:
                runLog.error(f"Cog ({cog}) doesn't exist. (cogsGuild.disableCog)")
                await ctx.message.add_reaction("⚠️")
        except Exception as e:
            runLog.error(f"Failed to disable cog ({cog}) for guild. (cogsGuild.disableCog)")
            await ctx.message.add_reaction("❌")

    @commands.command()
    @commands.is_owner()
    async def enableCog(self, ctx, *, cog):
        """
        Enable the use of the cog in specific guild.
        :param ctx:
        :param str cog: Cog name
        """
        try:
            value = queryCogList.loaded(cog)
            if value:
                insertCogGuild.cog(ctx.guild.id, cog, True)
                runLog.error(f"Enabled cog ({cog}) for guild. (cogsGuild.enableCog)")
                await ctx.message.add_reaction("✅")
            else:
                runLog.error(f"Cog ({cog}) doesn't exist. (cogsGuild.enableCog)")
                await ctx.message.add_reaction("⚠️")
        except Exception as e:
            runLog.error(f"Failed to enable cog ({cog}) for guild. (cogsGuild.enableCog)")
            await ctx.message.add_reaction("❌")

def setup(bot):
    bot.add_cog(cogGuild(bot))