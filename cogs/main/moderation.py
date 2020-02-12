'''
Name: Moderation
Description: Moderation commands
Last Updated: January 9, 2020
Created: October 30, 2019
'''
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
from util import commandchecks, logger

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ban (command)
    @commands.check(commandchecks.isAllowed)
    @commands.command(name="ban", description="Bans user from the guild.", usage="ban <user>")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member : discord.Member, *, reason=None):
        await member.ban(reason=reason)
        logger.logWrite('command-log.txt', f'{member} was banned by {ctx.message.author} for "{reason}"')

    # clear (command)
    @commands.check(commandchecks.isAllowed)
    @commands.command(name="clear", description="Clears x amount of messages from channel (including the message containing the command call).", usage="clear <#messages>", aliases=['purge'])
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount=1):
        await ctx.channel.purge(limit=amount+1)
        logger.logWrite('command-log.txt', f'{amount} message(s) were cleared by {ctx.message.author} in #{ctx.message.channel}')

    # kick (command)
    @commands.check(commandchecks.isAllowed)
    @commands.command(name="kick", description="Kicks user from the guild.", usage="kick <user>")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member : discord.Member, *, reason=None):
        await member.kick(reason=reason)
        logger.logWrite('command-log.txt', f'{member} was kicked by {ctx.message.author} for "{reason}"')

def setup(bot):
    bot.add_cog(Moderation(bot))