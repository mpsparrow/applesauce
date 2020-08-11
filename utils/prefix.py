from utils.config import readINI
from utils.database.actions import connect

def prefix(guildid: int):
    """
    Gets prefix
    :param int guildid: ID of guild
    """
    try:
        # looks for the location of a prefix in the database
        guildCol = connect()[readINI("config.ini")["MongoDB"]["database"]]["guilds"]
        guildData = guildCol.find_one({ "_id": guildid })
        return guildData["prefix"]
    except Exception:
        # returns config.ini default prefix
        return readINI("config.ini")["main"]["defaultPrefix"]