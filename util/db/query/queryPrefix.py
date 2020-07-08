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

        if len(data) > 0:
            for i in data:
                return i[0]
        else:
            try:
                conf = config.readINI('mainConfig.ini')
                return conf['main']['prefix']
            except exceptions.configError:
                raise exceptions.PrefixError(f"Unable to get prefix {guildID}. Raised from configError (util.db.query.queryPrefix.prefix)")
    except exceptions.dbQueryFail:
        raise exceptions.PrefixError(f"Unable to get prefix {guildID}. Raised from dbQueryFail (util.db.query.queryPrefix.prefix)")
        
