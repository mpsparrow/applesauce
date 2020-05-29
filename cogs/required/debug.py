# Debug cog
# Debug related commands for owner
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
import sys


class Debug(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="log", help="Displays the startup log.", aliases=["startupLog"])
    @commands.is_owner()
    async def startupLog(self, ctx):
        """
        Command to display start log.
        """
        await ctx.send(f"```{log.read(conf['logs']['start'])}```")

    @commands.command(name="ping", help="Pings the bot.")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def ping(self, ctx):
        """
        Command to ping the bot.
        """
        await ctx.send('pong!')

    @commands.command(name="debug", help="Versions and other debug information.")
    @commands.is_owner()
    async def debug(self, ctx):
        """
        Command to display versions and other debug information.
        """
        embed=discord.Embed(title='Debug', color=0xc1c100)
        embed.add_field(name="discord.py", value=discord.__version__, inline=False)
        embed.add_field(name="python", value=sys.version, inline=False)
        embed.add_field(name="OS", value=sys.platform, inline=False)
        await ctx.send(embed=embed)

    # guildid (command)
    @commands.command(name="guildid", help="Gets guild ID.", usage="guildid")
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