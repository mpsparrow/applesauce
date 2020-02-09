'''
Prefix related commands
'''
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
from utils import dbConnect, logger

class Prefix(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # change prefix (command)
    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def prefix(self, ctx, prefix: str):
        try:
            dbConnect.prefix(ctx.guild.id, prefix)
            await ctx.message.add_reaction("✅") # success
        except Exception as e:
            logger.errorRun("prefix.py prefix - error changing prefix")
            logger.normRun(e)
            await ctx.message.add_reaction("❌") # fail

def setup(bot):
    bot.add_cog(Prefix(bot))