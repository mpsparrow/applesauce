import discord
from discord.ext import commands
from discord.ext.commands import has_permissions

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # setup information and commands
    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def setup(self, ctx):
        embed=discord.Embed(title='Setup', description=f'Information and commands for setting up and configuring.', color=0xc1c100)
        embed.add_field(name='Commands', value='`random`, `random1`', inline=False)
        embed.set_footer(text='All non-admin commands have cooldowns.')
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Help(bot))
