import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
import sys

class Debug(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def debuginfo(self, ctx):
        await ctx.send('Useful commands for debugging and server info.')

    # commands
    # debug - prints some useful debugging information
    discordPyVersion = discord.__version__
    pythonVersion = sys.version

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def debug(self, ctx):
            embed=discord.Embed(title='Debug', color=0xc1c100)
            embed.add_field(name='discord.py version', value=f'{discordPyVersion}', inline=True)
            embed.add_field(name='python version', value=f'{pythonVersion}', inline=True)
            await ctx.send(embed=embed)

    # guildid - prints the guilds id
    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def guildid(self, ctx):
        await ctx.send(f'Guild id: {ctx.guild.id}')

def setup(bot):
    bot.add_cog(Debug(bot))
