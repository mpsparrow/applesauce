"""
Database connection
"""
import mysql.connector as mysql
from mysql.connector import errorcode
from util.log import runLog
from util import config, exceptions

def connect():
    """
    Connects to database
    :return: mysql.connector.connect object
    :raises dbConnectionFail: if database connection fails at all
    """
    try:
        conf = config.readINI('mainConfig.ini')
        cnx = mysql.connect(
            host = conf['mySQL']['host'],
            database = conf['mySQL']['database'], 
            user = conf['mySQL']['user'], 
            password = conf['mySQL']['password']
        )
    except mysql.Error as e:
        if e.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            runLog.error("Username or password incorrect. ER_ACCESS_DENIED_ERROR (connect.connect)")
        elif e.errno == errorcode.ER_BAD_DB_ERROR:
            runLog.error("Database does not exist. ER_BAD_DB_ERROR (connect.connect)")
        else:
            runLog.error("Database error. (connect.connect)")
            runLog.error(e)
        raise dbConnectionFail
    else:
        return cnx