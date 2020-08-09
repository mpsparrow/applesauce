import os
from utils.database.actions import isConnected, connect
from utils.logger import startLog
from utils.config import readINI

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

def configCheck():
    """
    Checks if config.ini contains proper variables
    """
    try:
        data = readINI("config.ini")["main"]
        if (len(data["discordToken"]) == 59) and (data["defaultPrefix"] is not "") and os.path.isdir(data["pluginFolder"]):
            startLog.info("Main config items located")
            return True
        return False
    except Exception as e:
        startLog.error("Unable to locate proper variables in config.ini")
        startLog.error(e)
        return False

def startupChecks():
    """
    Checks to make sure everything is in place before starting the bot
    """
    return databaseCheck() and configCheck()