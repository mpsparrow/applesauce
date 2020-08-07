from utils.database.actions import isConnected, connect
from utils.logger import startLog

def databaseCheck():
    """
    Checks connection to MongoDB database
    """
    try:
        c = connect()
        isConnected(c)
        startLog.info("Connected to MongoDB database")
        return True
    except Exception as e:
        startLog.error("Unable to connect to DB")
        startLog.error(e)
        return False

def startupChecks():
    """
    Checks to make sure everything is in place before starting the bot
    """
    return databaseCheck()