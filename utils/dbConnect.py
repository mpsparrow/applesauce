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
def SQLcommit(query, values, data=False):
    try:
        cnx = SQLconnect()
        cursor = cnx.cursor()
    except Exception as e:
        logger.errorRun("dbConnect.py SQLcommit - error connecting to database")
        logger.normRun(e)
    else:
        try:
            cursor.execute(query, values)
            if data == True:
                returnData = cursor.fetchall()
                cnx.commit()
                cnx.close()
                return returnData
            else:
                cnx.commit()
                cnx.close()
        except Exception as e:
            logger.errorRun("dbConnect.py SQLcommit - error committing query")
            logger.normRun(e)

# creates Prefix table
def tablePrefix():
    try:
        cnx = SQLconnect()
        cursor = cnx.cursor()
        cursor.execute("""CREATE TABLE `prefix` (
            `guild_id` BIGINT NOT NULL,
            `prefix` CHAR(50) NOT NULL,
            primary key (guild_id)
            )""")
    except:
        pass

# creates Ignore table
def tableIgnore():
    try:
        cnx = SQLconnect()
        cursor = cnx.cursor()
        cursor.execute("""CREATE TABLE `ignore` (
            `guild_id` BIGINT NOT NULL,
            `member_id` BIGINT NOT NULL, 
            `is_ignored` BOOLEAN NOT NULL,
            primary key (guild_id, member_id)
            )""")
    except:
        pass

# creates Commands table
def tableCommands():
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
    except:
        pass

# creates Cogs table
def tableCogs():
    try:
        cnx = SQLconnect()
        cursor = cnx.cursor()
        cursor.execute("""CREATE TABLE `cogs` (
            `cog_name` VARCHAR(50) NOT NULL,
            `is_enabled` BOOLEAN NOT NULL,
            primary key (cog_name)
            )""")
    except:
        pass

# creates Config table
def tableConfig():
    try:
        cnx = SQLconnect()
        cursor = cnx.cursor()
        cursor.execute("""CREATE TABLE `config` (
            `guild_id` BIGINT NOT NULL,
            `option_name` VARCHAR(50) NOT NULL,
            `value` LONGTEXT NOT NULL,
            primary key (guild_id, option_name)
            )""")
    except:
        pass

# add to Prefix table
def prefix(guildID: int, pref: str):
    try:
        tablePrefix()
        query = f"""INSERT INTO `prefix` (
            guild_id, prefix
        ) VALUES (%s, %s) ON DUPLICATE KEY UPDATE prefix = VALUES(prefix)"""
        values = (guildID, pref)
        SQLcommit(query, values)
    except Exception as e:
        logger.errorRun("dbConnect.py prefix - error")
        logger.normRun(e)

# add to Ignore table
def ignore(guildID: int, member: str, ignored: bool):
    try:
        tableIgnore()
        query = f"""INSERT INTO `ignore` (
            guild_id, member_id, is_ignored
        ) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE is_ignored = VALUES(is_ignored)"""
        values = (guildID, member, ignored)
        SQLcommit(query, values)
    except Exception as e:
        logger.errorRun("dbConnect.py ignore - error")
        logger.normRun(e)

# add to Commands table
def commands(guildID: int, name: str, enabled: bool):
    try:
        tableCommands()
        query = f"""INSERT INTO `commands` (
            guild_id, command_name, is_enabled
        ) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE is_enabled = VALUES(is_enabled)"""
        values = (guildID, name, enabled)
        SQLcommit(query, values)
    except Exception as e:
        logger.errorRun("dbConnect.py commands - error")
        logger.normRun(e)

# add to Cogs table
def cogs(name: str, enabled: bool):
    try:
        tableCogs()
        query = f"""INSERT INTO `cogs` (
            cog_name, is_enabled
        ) VALUES (%s, %s) ON DUPLICATE KEY UPDATE is_enabled = VALUES(is_enabled)"""
        values = (name, enabled)
        SQLcommit(query, values)
    except Exception as e:
        logger.errorRun("dbConnect.py cogs - error")
        logger.normRun(e)

# add to Config table
def configOptions(guildID: int, name: str, value: str):
    try:
        tableConfig()
        query = f"""INSERT INTO `config` (
            guild_id, option_name, value
        ) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE value = VALUES(value)"""
        values = (guildID, name, value)
        SQLcommit(query, values)
    except Exception as e:
        logger.errorRun("dbConnect.py config - error")
        logger.normRun(e)

# add to times_used in Commands table
def commandCount(guildID: int, name: str):
    try:
        query = f"""UPDATE `commands`
            SET times_used = IFNULL(times_used, 0) + 1
            WHERE guild_id = %s AND command_name = %s AND is_enabled = 1"""
        values = (guildID, name)
        SQLcommit(query, values)
    except Exception as e:
        logger.errorRun("dbConnect.py prefix - error")
        logger.normRun(e)