# Prefix cog
# Prefix changing commands
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
import dbInsert, logger

class Prefix(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # change prefix (command)
    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def prefix(self, ctx, prefix: str):
        try:
            dbInsert.prefix(ctx.guild.id, prefix)
            await ctx.message.add_reaction("✅")
        except Exception as e:
            logger.errorRun("prefix.py prefix - error changing prefix")
            logger.normRun(e)
            await ctx.message.add_reaction("❌")

def setup(bot):
    bot.add_cog(Prefix(bot))