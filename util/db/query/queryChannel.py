"""
Database query functions for channel
"""
from util.db.query import query
from util.log import runLog
from util import exceptions

def status(channelID: int, guildID: int, optionName: str):
    """
    Checks if channel is enabled in specific guild
    :param int channelID: ID of channel
    :param int guildID: ID of guild
    :param str optionName: Option name
    :return: True if enabled
    :rtype: bool
    """
    try:
        q = f"""SELECT is_enabled 
                FROM `channel` 
                WHERE guild_id = %s 
                AND channel_id = %s
                AND option_name = %s"""
        values = (guildID, cogName)
        data = query.queryV(q, values)
    except exceptions.dbQueryFail:
        runLog.error("Failed to check for channel status. dbQueryFail (queryChannel.enabled)")
        return False # return False so it disallows the action since an error occured
    else:
        if len(data) == 0:
            return False
        for i in data:
            return bool(i[0])