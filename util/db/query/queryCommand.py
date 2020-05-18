"""
Database query functions for commands
"""
from util.db.query import query
from util.log import runLog
from util import exceptions

def status(guildID: int, name: str):
    """
    Checks if command is enabled in specific guild
    :param int guildID: ID of guild
    :param str name: Command name
    :return: True if enabled
    :rtype: bool
    """
    try:
        query = f"""SELECT is_enabled 
                FROM `commands` 
                WHERE guild_id = %s 
                AND command_name = %s"""
        values = (guildID, name)
        data = query.queryV(query, values)
    except exceptions.dbQueryFail:
        runLog.error("Failed to check for command status. dbQueryFail (queryCommand.enabled)")
        return False # return False so it disallows the action since an error occured
    else:
        if len(data) == 0:
            return False
        for i in data:
            return bool(i[0])