"""
Database insertion functions for prefix
"""
from util.db import commit
from util.log import runLog
from util import exceptions

def prefix(guildID: int, pref: str):
    """
    Sets prefix for guild
    :param int guildID: ID of guild
    :param str pref: Prefix for guild
    :raises PrefixError: if fails to set prefix
    """
    try:
        query = f"""INSERT INTO `prefix` (
            guild_id, prefix
        ) VALUES (%s, %s) ON DUPLICATE KEY UPDATE prefix = VALUES(prefix)"""
        values = (guildID, pref)
        commit.commitV(query, values)
    except exceptions.dbCommitFail:
        runLog.error("Error setting prefix. (insertPrefix.prefix)")
        raise exceptions.PrefixError