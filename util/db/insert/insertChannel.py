"""
Database insertion functions for channel
"""
from util.db import commit
from util.log import runLog
from util import exceptions

def channel(channelID: str, guildID: int, optionName: str, enabled: bool):
    """
    Adds/Updates channels in db.
    :param int guildID: ID of guild
    :param str channelID: ID of channel
    :param str optionName: Name of options
    :param bool enabled: Enabled or disabled bool
    """
    try:
        query = f"""INSERT INTO `channel` (
            channel_id, guild_id, option_name, is_enabled
        ) VALUES (%s, %s, %s, %s) ON DUPLICATE KEY UPDATE is_enabled = VALUES(is_enabled)"""
        values = (channelID, guildID, optionName, enabled)
        commit.commitV(query, values)
    except exceptions.dbCommitFail:
        runLog.error(f"Error adding/updating {name} channel (util.db.insert.insertChannel.cog)")