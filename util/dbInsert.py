# Insert functions for database.
from util import dbConnect, dbTables

# Inserts into prefix table
def prefix(guildID: int, pref: str):
    try: dbTables.prefix()
    except: pass

    query = f"""INSERT INTO `prefix` (
        guild_id, prefix
    ) VALUES (%s, %s) ON DUPLICATE KEY UPDATE prefix = VALUES(prefix)"""
    values = (guildID, pref)
    dbConnect.commit(query, values)

# Inserts into ignore table
def ignore(guildID: int, member: str, ignored: bool):
    try: dbTables.ignore()
    except: pass

    query = f"""INSERT INTO `ignore` (
        guild_id, member_id, is_ignored
    ) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE is_ignored = VALUES(is_ignored)"""
    values = (guildID, member, ignored)
    dbConnect.commit(query, values)

# Inserts into commands table
def commands(guildID: int, name: str, enabled: bool):
    try: dbTables.commands()
    except: pass

    query = f"""INSERT INTO `commands` (
        guild_id, command_name, is_enabled
    ) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE is_enabled = VALUES(is_enabled)"""
    values = (guildID, name, enabled)
    dbConnect.commit(query, values)

# Inserts into cogs table
def cogs(name: str, enabled: bool):
    try: dbTables.cogs()
    except: pass

    query = f"""INSERT INTO `cogs` (
        cog_name, is_enabled
    ) VALUES (%s, %s) ON DUPLICATE KEY UPDATE is_enabled = VALUES(is_enabled)"""
    values = (name, enabled)
    dbConnect.commit(query, values)

# Inserts into config table
def config(guildID: int, name: str, value: str):
    try: dbTables.config()
    except: pass

    query = f"""INSERT INTO `config` (
        guild_id, option_name, value
    ) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE value = VALUES(value)"""
    values = (guildID, name, value)
    dbConnect.commit(query, values)

# Updated times_used in commands table
def commandCount(guildID: int, name: str):
    try:
        query = f"""UPDATE `commands`
            SET times_used = IFNULL(times_used, 0) + 1
            WHERE guild_id = %s AND command_name = %s AND is_enabled = 1"""
        values = (guildID, name)
        dbConnect.commit(query, values)
    except:
        pass # command does not exist