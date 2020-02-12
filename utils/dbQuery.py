'''
mySQL query commands
'''
from utils import dbConnect, logger, config
import mysql.connector as mysql
from mysql.connector import errorcode

# gets guild prefix
def prefix(guildID: int):
    try:
        try:
            query = f"""SELECT prefix FROM `prefix` WHERE guild_id = {guildID}"""
            values = ()
            data = dbConnect.SQLcommit(query, values, True)
            for i in data:
                return i[0]
        except:
            pass
        try:
            conf = config.read('mainConfig.ini')
            return conf['main']['prefix']
        except:
            pass
    except Exception as e:
        logger.errorRun("dbQuery.py prefix - unable to obtain a prefix")
        logger.normRun(e)

# gets ignored player
def ignore(guildID: int, memberID: int):
    try:
        query = f"""SELECT is_ignored FROM `ignore` WHERE guild_id = %s AND member_id = %s"""
        values = (guildID, memberID)
        data = dbConnect.SQLcommit(query, values, True)
        if len(data) == 0:
            return False
        else:
            for i in data:
                return bool(i[0])
    except Exception as e:
        logger.errorRun("dbQuery.py ignore - unable to obtain ignore value")
        logger.normRun(e)

# gets guild command
def command(guildID: int, name: str):
    try:
        query = f"""SELECT is_enabled FROM `commands` WHERE guild_id = %s AND command_name = %s"""
        values = (guildID, name)
        data = dbConnect.SQLcommit(query, values, True)
        if len(data) == 0:
            return False
        else:
            for i in data:
                return bool(i[0])
    except Exception as e:
        logger.errorRun("dbQuery.py command - unable to obtain command value")
        logger.normRun(e)

# gets cog
def cog(name: str):
    try:
        query = f"""SELECT is_enabled FROM `cogs` WHERE cog_name = '{name}'"""
        values = ()
        data = dbConnect.SQLcommit(query, values, True)
        for i in data:
            return bool(i[0])
    except Exception as e:
        logger.errorRun("dbQuery.py cog - unable to obtain cog value")
        logger.normRun(e)

# get config
def config(guildID: int, name: str):
    try:
        query = f"""SELECT value FROM `config` WHERE option_name = %s AND guild_id = %s"""
        values = (name, guildID)
        data = dbConnect.SQLcommit(query, values, True)
        for i in data:
            return i[0]
    except Exception as e:
        logger.errorRun("dbQuery.py config - unable to obtain config option")
        logger.normRun(e)

# gets command times_used
def commandCount(guildID: int, name: str):
    try:
        query = f"""SELECT times_used FROM `commands` WHERE guild_id = %s AND command_name = %s"""
        values = (guildID, name)
        data = dbConnect.SQLcommit(query, values, True)
        for i in data:
            return i[0]
    except Exception as e:
        logger.errorRun("dbQuery.py commandCount - unable to obtain times_used")
        logger.normRun(e)