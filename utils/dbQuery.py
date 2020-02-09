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
            cnx = dbConnect.SQLconnect()
            cursor = cnx.cursor()
            query = f"""SELECT prefix FROM `prefix` WHERE guild_id = {guildID}"""
            cursor.execute(query)
            data = cursor.fetchall()
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
        cnx = dbConnect.SQLconnect()
        cursor = cnx.cursor()
        query = f"""SELECT is_ignored FROM `ignore` WHERE guild_id = {guildID} AND member_id = {memberID}"""
        cursor.execute(query)
        data = cursor.fetchall()
        if len(data) == 0:
            return False
        else:
            for i in data:
                return bool(i[0])
    except Exception as e:
        logger.errorRun("dbQuery.py ignore - unable to obtain ignore")
        logger.normRun(e)