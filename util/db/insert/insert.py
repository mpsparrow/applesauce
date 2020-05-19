# Insert functions for database.
from util import dbConnect, dbTables

# Inserts into ignore table
def ignore(guildID: int, guild_name: str, member: str, ignored: bool):
    try: dbTables.ignore()
    except: pass

    query = f"""INSERT INTO `ignore` (
        guild_id, guild_name, member_id, is_ignored
    ) VALUES (%s, %s, %s, %s) 
    ON DUPLICATE KEY UPDATE 
    is_ignored = VALUES(is_ignored),
    guild_name = VALUES(guild_name)"""
    values = (guildID, guild_name, member, ignored)
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

# Archive insert
def archive(guildID: int, channel: int, role: int, pins: bool, toggle: bool):
    try: dbTables.archive()
    except: pass

    query = f"""INSERT INTO `archive` (
        guild_id, channel, role, pins, toggle
    ) VALUES (%s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE channel = VALUES(channel), role = VALUES(role), pins = VALUES(pins), toggle = VALUES(toggle)"""
    values = (guildID, channel, role, pins, toggle)
    dbConnect.commit(query, values)

def archiveChannel(guildID: int, channel: int):
    try: dbTables.archive()
    except: pass

    query = f"""INSERT INTO `archive` (
        guild_id, channel
    ) VALUES (%s, %s) ON DUPLICATE KEY UPDATE channel = VALUES(channel)"""
    values = (guildID, channel)
    dbConnect.commit(query, values)

def archiveRole(guildID: int, role: int):
    try: dbTables.archive()
    except: pass

    query = f"""INSERT INTO `archive` (
        guild_id, role
    ) VALUES (%s, %s) ON DUPLICATE KEY UPDATE role = VALUES(role)"""
    values = (guildID, role)
    dbConnect.commit(query, values)

def archivePins(guildID: int, pins: bool):
    try: dbTables.archive()
    except: pass

    query = f"""INSERT INTO `archive` (
        guild_id, pins
    ) VALUES (%s, %s) ON DUPLICATE KEY UPDATE pins = VALUES(pins)"""
    values = (guildID, pins)
    dbConnect.commit(query, values)

def archiveToggle(guildID: int, toggle: bool):
    try: dbTables.archive()
    except: pass

    query = f"""INSERT INTO `archive` (
        guild_id, toggle
    ) VALUES (%s, %s) ON DUPLICATE KEY UPDATE toggle = VALUES(toggle)"""
    values = (guildID, toggle)
    dbConnect.commit(query, values)

def leaderboard(guild_id: int, guild_name: str, member_id: int, member_name: str, level: int, points: int, next_level: int, last_added, message_count: int):
    try: dbTables.archive()
    except: pass

    query = f"""INSERT INTO `leaderboard` (
        guild_id, guild_name, member_id, member_name, level, points, next_level, last_added, message_count
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) 
        ON DUPLICATE KEY UPDATE 
        guild_name = VALUES(guild_name), 
        member_name = VALUES(member_name), 
        level = VALUES(level), 
        points = VALUES(points), 
        next_level = VALUES(next_level),
        last_added = VALUES(last_added),
        message_count = VALUES(message_count)"""
    values = (guild_id, guild_name, member_id, member_name, level, points, next_level, last_added, message_count)
    dbConnect.commit(query, values)