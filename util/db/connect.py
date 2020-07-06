"""
Database connection
"""
import mysql.connector as mysql
from mysql.connector import errorcode
from util.log import runLog
from util import exceptions
from util import config

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
            runLog.error("ER_ACCESS_DENIED_ERROR username or password is incorrect (util.db.connect.connect)")
        elif e.errno == errorcode.ER_BAD_DB_ERROR:
            runLog.error("ER_BAD_DB_ERROR database does not exist (util.db.connect.connect)")
        else:
            runLog.error("database error (util.db.connect.connect)")
            runLog.error(e)
        raise exceptions.dbConnectionFail("failed to connect to database (util.db.connect.connect)")
    else:
        return cnx