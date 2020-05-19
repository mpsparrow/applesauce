# Prefix cog
# Prefix changing commands
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
from util.db.insert import insertPrefix
from util import exceptions

class Prefix(commands.Cog):
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