"""
Command checks
"""
from util.db.insert import insertCommand
from util.db.query import queryIgnore, queryCommand
from util.log import runLog

def isAllowed(ctx):
    """
    Authorizes commands. Checks if author is ignored on guild. Checks if command is enabled on guild.
    :param ctx: Context
    :return: True if allowed
    :rtype: bool
    """
    try:
        guildID = ctx.guild.id
        name = ctx.command.qualified_name
        author = ctx.message.author.id
        value = queryCommand.status(guildID, name) and not(queryIgnore.status(guildID, author))

        # ups the command usage counter if command checks all pass
        if value:
            insertCommand.count(guildID, name)
    except Exception:
        runLog.error("isAllowed error (checks.command)")
        return False
    else:
        return value