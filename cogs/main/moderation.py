import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
from util.checks import command

class Moderation(commands.Cog):
    """
    Moderation controls and commands.
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.check(command.isAllowed)
    @commands.command(name="ban", description="Bans user from the guild.", usage="ban <user> <reason>")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member : discord.Member, *, reason=None):
        await member.ban(reason=reason)

    @commands.check(command.isAllowed)
    @commands.command(name="clear", description="Clears x amount of messages from channel (including the message containing the command call).", usage="clear <#messages>", aliases=['purge'])
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount=1):
        await ctx.channel.purge(limit=amount+1)

    @commands.check(command.isAllowed)
    @commands.command(name="kick", description="Kicks user from the guild.", usage="kick <user>")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member : discord.Member, *, reason=None):
        await member.kick(reason=reason)

def setup(bot):
    bot.add_cog(Moderation(bot))