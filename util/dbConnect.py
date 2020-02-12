# Database connection and query functions.
import mysql.connector as mysql
from mysql.connector import errorcode
from util import logger, config

# Connects to mySQL database
def connect():
    try:
        conf = config.readINI('mainConfig.ini')
        cnx = mysql.connect(
            host = conf['mySQL']['host'],
            database = conf['mySQL']['dbname'], 
            user = conf['mySQL']['user'], 
            password = conf['mySQL']['password']
        )
        return cnx
    except mysql.Error as e:
        if e.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            logger.errorRun("dbConnect.py SQLconnect - Something is wrong with the username or password")
            logger.normRun(e)
        elif e.errno == errorcode.ER_BAD_DB_ERROR:
            logger.errorRun("dbConnect.py SQLconnect - Database does not exist")
            logger.normRun(e)
        else:
            logger.errorRun("dbConnect.py SQLconnect - error")
            logger.normRun(e)

# Queries database
# data controls whether to return query data
def commit(query, values, data=False):
    try:
        cnx = connect()
        cursor = cnx.cursor()
        cursor.execute(query, values)

        if data:
            returnData = cursor.fetchall()
            cnx.commit()
            cnx.close()
            return returnData
        else:
            cnx.commit()
            cnx.close()
    except Exception as e:
        logger.errorRun("dbConnect.py SQLcommit - error committing query")
        logger.errorRun(e)