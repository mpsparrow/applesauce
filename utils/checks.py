from utils.database.actions import isConnected, connect

def startupchecks():
    """
    Checks to make sure everything is in place before starting the bot
    """
    return isConnected(connect())