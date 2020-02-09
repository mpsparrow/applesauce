'''
mySql connection module
'''
from utils import logger, config
import mysql.connector as mysql
from mysql.connector import errorcode

# makes connection to mySQL database
def SQLconnect():
    try:
        conf = config.read('mainConfig.ini')
        cnx = mysql.connect(
            host = conf['mySQL']['host'],
            database = conf['mySQL']['dbname'], 
            user = conf['mySQL']['user'], 
            password = conf['mySQL']['password']
        )
        return cnx
    except mysql.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            logger.errorRun("dbConnect.py SQLconnect - Something is wrong with the username or password")
            logger.normRun(err)
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            logger.errorRun("dbConnect.py SQLconnect - Database does not exist")
            logger.normRun(err)
        else:
            logger.errorRun("dbConnect.py SQLconnect - error")
            logger.normRun(err)

# adds data to database
def SQLcommit(query, values):
    try:
        cnx = SQLconnect()
        cursor = cnx.cursor()
    except Exception as e:
        logger.errorRun("dbConnect.py SQLcommit - error connecting to database")
        logger.normRun(e)
    else:
        try:
            cursor.execute(query, values)
            cnx.commit()
            cnx.close()
        except Exception as e:
            logger.errorRun("dbConnect.py SQLcommit - error committing query")
            logger.normRun(e)

# creates Prefix table
def tablePrefix(guildID: int):
    try:
        cnx = SQLconnect()
        cursor = cnx.cursor()
        cursor.execute("""CREATE TABLE `prefix` (
            `guild_id` BIGINT NOT NULL,
            `prefix` CHAR(50) NOT NULL,
            primary key (guild_id)
            )""")
    except Exception as e:
        logger.errorRun("dbConnect.py tablePrefix - error creating table")
        logger.normRun(e)

# creates Ignore table
def tableIgnore(guildID: int):
    try:
        cnx = SQLconnect()
        cursor = cnx.cursor()
        cursor.execute("""CREATE TABLE `ignore` (
            `guild_id` BIGINT NOT NULL,
            `member_id` BIGINT NOT NULL, 
            `is_ignored` BOOLEAN NOT NULL,
            primary key (guild_id, member_id)
            )""")
    except Exception as e:
        logger.errorRun("dbConnect.py tableIgnore - error creating table")
        logger.normRun(e)

# created Commands table
def tableCommands(guildID: int):
    try:
        cnx = SQLconnect()
        cursor = cnx.cursor()
        cursor.execute("""CREATE TABLE `commands` (
            `guild_id` BIGINT NOT NULL,
            `command_name` VARCHAR(30) NOT NULL, 
            `is_enabled` BOOLEAN NOT NULL,
            `times_used` BIGINT,
            primary key (guild_id, command_name)
            )""")
    except Exception as e:
        logger.errorRun("dbConnect.py tableCommands - error creating table")
        logger.normRun(e)

# main function to add to Prefix table
def prefix(guildID: int, pref: str):
    try:
        tablePrefix(guildID)
        query = f"""INSERT INTO `prefix` (
            guild_id, prefix
        ) VALUES (%s, %s) ON DUPLICATE KEY UPDATE prefix = VALUES(prefix)"""
        values = (guildID, pref)
        SQLcommit(query, values)
    except Exception as e:
        logger.errorRun("dbConnect.py prefix - error")
        logger.normRun(e)

# main function to add to Ignore table
def ignore(guildID: int, member: str, ignored: bool):
    try:
        tableIgnore(guildID)
        query = f"""INSERT INTO `ignore` (
            guild_id, member_id, is_ignored
        ) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE is_ignored = VALUES(is_ignored)"""
        values = (guildID, member, ignored)
        SQLcommit(query, values)
    except Exception as e:
        logger.errorRun("dbConnect.py prefix - error")
        logger.normRun(e)

# main function to add to Commands table
def commands(guildID: int, name: str, enabled: bool, used: int):
    try:
        tableCommands(guildID)
        query = f"""INSERT INTO `commands` (
            guild_id, command_name, is_enabled, times_used
        ) VALUES (%s, %s, %s, %s) ON DUPLICATE KEY UPDATE is_enabled = VALUES(is_enabled)"""
        values = (guildID, name, enabled, used)
        SQLcommit(query, values)
    except Exception as e:
        logger.errorRun("dbConnect.py prefix - error")
        logger.normRun(e)