'''
Commands to ignore users
 *ignore/unignore
'''
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
from utils import dbConnect, logger

class Ignore(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ignore user for guild (command)
    @commands.command()
    @commands.is_owner()
    async def ignore(self, ctx, member : discord.Member):
        try:
            dbConnect.ignore(ctx.guild.id, member.id, True)
            await ctx.message.add_reaction("✅") # success
        except:
            await ctx.message.add_reaction("❌") # fail

    # unignore user for guild (command)
    @commands.command()
    @commands.is_owner()
    async def unignore(self, ctx, member : discord.Member):
        try:
            dbConnect.ignore(ctx.guild.id, member.id, False)
            await ctx.message.add_reaction("✅") # success
        except:
            await ctx.message.add_reaction("❌") # fail
        
def setup(bot):
    bot.add_cog(Ignore(bot))