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