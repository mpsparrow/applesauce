from utils.database.actions import isConnected, connect

def startupchecks():
    """
    Checks to make sure everything is in place before starting the bot
    """
    try:
        c = connect()
        isConnected(c)
        print("worked")
        return True
    except Exception as e:
        print("something")
        print(e)
        return False