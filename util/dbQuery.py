# Query database functions
import mysql.connector as mysql
from mysql.connector import errorcode
from util import dbConnect, logger, config, dbTables


# Prefix based on guild id
def prefix(guildID: int):
    try:
        query = f"""SELECT prefix FROM `prefix` WHERE guild_id = {guildID}"""
        values = ()
        data = dbConnect.commit(query, values, True)
        for i in data:
            return i[0]
    except:
        pass
    try:
        conf = config.read('mainConfig.ini')
        return conf['main']['prefix']
    except:
        pass

# Ignored member value based on guild id and member id
def ignore(guildID: int, memberID: int):
    query = f"""SELECT is_ignored FROM `ignore` WHERE guild_id = %s AND member_id = %s"""
    values = (guildID, memberID)
    data = dbConnect.commit(query, values, True)
    if len(data) == 0:
        return False
    else:
        for i in data:
            return bool(i[0])

# Command enabled value based on guild id and command name
def command(guildID: int, cmd: str):
    query = f"""SELECT is_enabled FROM `commands` WHERE guild_id = %s AND command_name = %s"""
    values = (guildID, cmd)
    data = dbConnect.commit(query, values, True)
    if len(data) == 0:
        return False
    else:
        for i in data:
            return bool(i[0])

# Cog enabled value based on cog name
def cogEnabled(name: str):
    query = f"""SELECT is_enabled FROM `cogs` WHERE cog_name = '{name}'"""
    values = ()
    data = dbConnect.commit(query, values, True)
    for i in data:
        return bool(i[0])

# Cog loaded value based on cog name
def cogLoaded(name: str):
    query = f"""SELECT is_loaded FROM `cogs` WHERE cog_name = '{name}'"""
    values = ()
    data = dbConnect.commit(query, values, True)
    for i in data:
        return bool(i[0])

# Config variable value based on guild id and variable name
def config(guildID: int, name: str):
    query = f"""SELECT value FROM `config` WHERE option_name = %s AND guild_id = %s"""
    values = (name, guildID)
    data = dbConnect.commit(query, values, True)
    for i in data:
        return i[0]

# Command usage based on guild id and command name
def commandCount(guildID: int, cmd: str):
    query = f"""SELECT times_used FROM `commands` WHERE guild_id = %s AND command_name = %s"""
    values = (guildID, cmd)
    data = dbConnect.commit(query, values, True)
    for i in data:
        return i[0]

# Archive
def archive(guildID: int):
    try: dbTables.archive()
    except: pass

    query = f"""SELECT * FROM `archive` WHERE guild_id = {guildID}"""
    values = ()
    data = dbConnect.commit(query, values, True)
    return data[0]