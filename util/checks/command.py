"""
Command checks
"""
from util.db.query import queryIgnore, queryCogGuild
from util.log import runLog

def isAllowed(ctx):
    runLog.info("test")
    """
    Authorizes commands. Checks if author is ignored on guild. Checks if cog is enabled on guild.
    :param ctx: Context
    :return: True if allowed
    :rtype: bool
    """
    try:
        runLog.info("1")
        guildID = ctx.guild.id
        cogName = ctx.command.cog.qualified_name
        print(cogName)
        author = ctx.message.author.id
        runLog.info("2")
        value = queryCogGuild.status(guildID, cogName)
        print(value)
        value2 = not(queryIgnore.status(guildID, author))
        print(value2)
    except Exception:
        runLog.error("isAllowed error (checks.command)")
        return False
    else:
        return value