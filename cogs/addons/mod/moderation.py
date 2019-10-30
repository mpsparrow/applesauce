import discord
from discord.ext import commands
from discord.ext.commands import has_permissions

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # commands
    # ban command
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member : discord.Member, *, reason=None):
        await member.ban(reason=reason)
        print(f'{member} was banned by {ctx.message.author} for "{reason}"')

    # clear/purge command
    @commands.command(aliases=['purge'])
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount=1):
        await ctx.channel.purge(limit=amount+1)
        print(f'{amount} message(s) were cleared by {ctx.message.author} in #{ctx.message.channel}')

    # kick command
    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member : discord.Member, *, reason=None):
        await member.kick(reason=reason)
        print(f'{member} was kicked by {ctx.message.author} for "{reason}"')

def setup(bot):
    bot.add_cog(Moderation(bot))
