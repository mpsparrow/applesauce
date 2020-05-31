"""
Database query functions for prefix
"""
from util.db.query import query
from util.log import runLog
from util import exceptions
from util import config

def prefix(guildID: int):
    """
    Gets prefix from db for guild. If prefix not found returns the default prefix.
    :param int guildID: ID of guild
    :return: prefix
    :rtype: str
    :raises PrefixError: if unable to get a prefix
    """
    try:
        q = f"""SELECT prefix FROM `prefix` WHERE guild_id = {guildID}"""
        data = query.query(q)
        for i in data:
            return i[0]
    except exceptions.dbQueryFail:
        try:
            conf = config.readINI('mainConfig.ini')
            return conf['main']['prefix']
        except exceptions.configReadError:
            runLog.error(f"Unable to get prefix {guildID} (queryPrefix.prefix)")
            raise exceptions.PrefixError