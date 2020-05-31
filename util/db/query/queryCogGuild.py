"""
Database query functions for commands
"""
from util.db.query import query
from util.log import runLog
from util import exceptions

def status(guildID: int, cogName: str):
    """
    Checks if cog is enabled in specific guild
    :param int guildID: ID of guild
    :param str cogName: Cog name
    :return: True if enabled
    :rtype: bool
    """
    try:
        q = f"""SELECT is_enabled 
                FROM `cogs_guild` 
                WHERE guild_id = %s 
                AND cog_name = %s"""
        values = (guildID, cogName)
        data = query.queryV(q, values)
    except exceptions.dbQueryFail:
        runLog.error("Failed to check for cog status. dbQueryFail (queryCogGuild.enabled)")
        return False # return False so it disallows the action since an error occured
    else:
        if len(data) == 0:
            return False
        for i in data:
            return bool(i[0])