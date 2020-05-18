"""
Database query functions for prefix
"""
from util.db import query
from util.log import runLog
from util import exceptions, config

def prefix(guildID: int):
    """
    Gets prefix from db for guild. If prefix not found returns the default prefix.
    :param int guildID: ID of guild
    :return: prefix
    :rtype: str
    :raises PrefixError: if unable to get a prefix
    """
    try:
        query = f"""SELECT prefix FROM `prefix` WHERE guild_id = %s"""
        values = (guildID)
        data = query.queryV(query, values)
        for i in data:
            return i[0]
    except dbQueryFail:
        try:
            conf = config.readINI('mainConfig.ini')
            return conf['main']['prefix']
        except configReadError:
            runLog.error(f"Unable to get prefix {guildID} (queryPrefix.prefix)")
            raise PrefixError