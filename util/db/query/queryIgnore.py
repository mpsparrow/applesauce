"""
Database query functions for ignore
"""
from util.db.query import query
from util.log import runLog
from util import exceptions

def status(guildID: int, memberID: int):
    """
    Checks if user is ignored in specific guild
    :param int guildID: ID of guild
    :param int memberID: ID of member
    :return: True if ignored
    :rtype: bool
    """
    try:
        query = f"""SELECT is_ignored 
                FROM `ignore` 
                WHERE guild_id = %s 
                AND member_id = %s"""
        values = (guildID, memberID)
        data = query.queryV(query, values)
    except exceptions.dbQueryFail:
        runLog.error("Failed to check for ignored user. dbQueryFail (queryIgnore.ignore)")
        return True # return True so it disallows the action since an error occured
    else:
        if len(data) == 0:
            return False
        for i in data:
            return bool(i[0])