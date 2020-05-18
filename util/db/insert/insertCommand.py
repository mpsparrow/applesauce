"""
Database insertion functions for commands
"""
from util.db import commit
from util.log import runLog
from util import exceptions

def command(guildID: int, name: str, enabled: bool):
    """
    Adds/Updates command in db.
    :param int guildID: ID of guild
    :param int name: Name of command
    :param bool enabled: If command is enabled for use. True = Yes
    """
    try:
        query = f"""INSERT INTO `commands` (
            guild_id, command_name, is_enabled
        ) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE is_enabled = VALUES(is_enabled)"""
        values = (guildID, name, enabled)
        commit.commitV(query, values)
    except exceptions.dbCommitFail:
        runLog.error(f"Error adding/updating {name} command. dbCommitFail (insertCommand.command)")

def count(guildID: int, name: str):
    """
    Counts command usage number up by 1 (per guild basis).
    :param int guildID: ID of guild
    :param int name: Name of command
    """
    try:
        query = f"""UPDATE `commands`
            SET times_used = IFNULL(times_used, 0) + 1
            WHERE guild_id = %s AND command_name = %s AND is_enabled = 1"""
        values = (guildID, name)
        commit.commitV(query, values)
    except exceptions.dbCommitFail:
        runLog.error(f"Error counting {name} command. dbCommitFail (insertCommand.count)")