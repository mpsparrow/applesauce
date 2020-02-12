# Ignore cog
# Commands to ignore users
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
from util import dbInsert, logger

class Ignore(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ignore user for guild (command)
    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def ignore(self, ctx, member : discord.Member):
        try:
            dbInsert.ignore(ctx.guild.id, member.id, True)
            await ctx.message.add_reaction("✅")
        except:
            await ctx.message.add_reaction("❌")

    # unignore user for guild (command)
    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def unignore(self, ctx, member : discord.Member):
        try:
            dbInsert.ignore(ctx.guild.id, member.id, False)
            await ctx.message.add_reaction("✅")
        except:
            await ctx.message.add_reaction("❌")
        
def setup(bot):
    bot.add_cog(Ignore(bot))