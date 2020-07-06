import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
import db.insert.insertPrefix
import util.exceptions

class Prefix(commands.Cog):
    """
    Prefix changing and management.
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def prefix(self, ctx, prefix: str):
        try:
            insertPrefix.prefix(ctx.guild.id, prefix)
        except exception.PrefixError:
            await ctx.message.add_reaction("❌")
        else:
            await ctx.message.add_reaction("✅")

def setup(bot):
    bot.add_cog(Prefix(bot))