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
        logger.errorRun("dbQuery.py ignore - unable to obtain ignore")
        logger.normRun(e)

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
        logger.errorRun("dbQuery.py command - unable to obtain command")
        logger.normRun(e)

def commandCount(guildID: int, name: str):
    try:
        query = f"""SELECT times_used FROM `commands` WHERE guild_id = %s AND command_name = %s"""
        values = (guildID, name)
        data = dbConnect.SQLcommit(query, values, True)
        for i in data:
            return bool(i[0])
    except Exception as e:
        logger.errorRun("dbQuery.py commandCount - unable to obtain times_used")
        logger.normRun(e)