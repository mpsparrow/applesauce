import discord
from discord.ext import commands
from cogs.utils import checks
import random
import datetime

class UserInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # userinfo command
    @commands.check(checks.allowedGuild)
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(name="userinfo", description="displayed information about user", usage="userinfo user", aliases=["player", "playerinfo", "user"])
    async def userinfo(self, ctx, *, user: discord.Member = None):
        if not user:
            user = ctx.author

        embed=discord.Embed(title=f'{user.name}#{user.discriminator}', description=f'{user.display_name}', color=user.color)
        embed.set_thumbnail(url=user.avatar_url)
        embed.add_field(name='Join Date: ', value=f'{user.joined_at.strftime("%B %d, %Y @%H:%M:%S")}', inline=True)
        embed.add_field(name='Account Created: ', value=f'{user.created_at.strftime("%B %d, %Y @%H:%M:%S")}', inline=True)
        embed.set_footer(text=f'ID: {user.id}')
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(UserInfo(bot))