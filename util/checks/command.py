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
        value = queryCogGuild.status(guildID, cogName)
        print(value)
        value2 = not(queryIgnore.status(guildID, author)
        print(value2)
    except Exception:
        runLog.error("isAllowed error (checks.command)")
        return False
    else:
        return value