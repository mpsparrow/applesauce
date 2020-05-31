"""
Command checks
"""
from util.db.query import queryIgnore, queryCogGuild
from util.log import runLog

def isAllowed(ctx):
    """
    Authorizes commands. Checks if author is ignored on guild. Checks if cog is enabled on guild.
    :param ctx: Context
    :return: True if allowed
    :rtype: bool
    """
    try:
        guildID = ctx.guild.id
        cogName = ctx.command.cog
        author = ctx.message.author.id
        value = queryCogGuild.status(guildID, cogName) and not(queryIgnore.status(guildID, author))
    except Exception:
        runLog.error("isAllowed error (checks.command)")
        return False
    else:
        return value