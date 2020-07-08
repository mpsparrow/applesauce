"""
Database insertion functions for commands
"""
from util.db import commit
from util.log import runLog
from util import exceptions

def cog(guildID: int, cogName: str, enabled: bool):
    """
    Adds/Updates cog in db.
    :param int guildID: ID of guild
    :param int cogName: Name of cog
    :param bool enabled: If cog is enabled for use. True = Yes
    :raises CogFail: If adding/updating the cog in db fails
    """
    try:
        query = f"""INSERT INTO `cogs_guild` (
            guild_id, cog_name, is_enabled
        ) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE is_enabled = VALUES(is_enabled)"""
        values = (guildID, cogName, enabled)
        commit.commitV(query, values)
    except exceptions.dbCommitFail:
        raise exceptions.CogFail(f"Error adding/updating {name} cog. Raised from dbCommitFail (util.db.insert.insertCogGuild.cog)")