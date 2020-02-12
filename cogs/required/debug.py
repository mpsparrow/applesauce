# Debug cog
# Debug related commands for owner
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
import sys

class Debug(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # debug (command)
    @commands.command(name="debug", description="Version and debug information.", usage="debug")
    @commands.is_owner()
    async def debug(self, ctx):
        embed=discord.Embed(title='Debug', color=0xc1c100)
        embed.add_field(name='discord.py version', value=f'{discord.__version__}', inline=False)
        embed.add_field(name='python version', value=f'{sys.version}', inline=False)
        await ctx.send(embed=embed)

    # guildid (command)
    @commands.command(name="guildid", description="Gets guild ID.", usage="guildid")
    @commands.is_owner()
    async def guildid(self, ctx):
        await ctx.send(f'Guild id: {ctx.guild.id}')

    # latency (command)
    @commands.command(name="latency", description="Gets latency to server.", usage="latency")
    @commands.is_owner()
    async def latency(self, ctx):
        await ctx.send(str(round(self.bot.latency * 1000)) + 'ms')

    # close (command)
    @commands.command(name="close", description="Shuts down bot.", usage="close", aliases=['shutdown', 'restart', 'kill'])
    @commands.is_owner()
    async def close(self, ctx):
        await ctx.send("shutting down....")
        await self.bot.close()

def setup(bot):
    bot.add_cog(Debug(bot))