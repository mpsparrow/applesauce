"""
Checks to run through on startup of bot
"""
from util import config
from util.log import startLog
from util.db import tables, connect
from util.db.query import query
from util import exceptions

def checks():
    """
    Runs through pile of startup checks and returns True if they all pass
    """

    # mainConfig.ini access check
    try:
        conf = config.readINI("mainConfig.ini")
        startLog.proceed("mainConfig.ini found", console=True)
    except exceptions.configError:
        startLog.error("mainConfig.ini missing or unable to load configReadError", console=True)
        return False

    # botname in mainConfig.ini
    try:
        name = conf["main"]["botname"]
    except Exception:
        startLog.error("botname not found in mainConfig.ini", console=True)
        return False
    else:
        startLog.proceed("botName found", console=True)

    # default prefix in mainConfig.ini
    try:
        prefix = conf["main"]["prefix"]
    except Exception:
        startLog.error("prefix not found in mainConfig.ini", console=True)
        return False
    else:
        startLog.proceed("botName found", console=True)

    # token in mainConfig.ini
    try:
        prefix = conf["main"]["discordToken"]
    except Exception:
        startLog.error("token not found in mainConfig.ini", console=True)
        return False
    else:
        startLog.proceed("token found", console=True)

    # db information
    try:
        host = conf["mySQL"]["host"]
        database = conf["mySQL"]["database"]
        user = conf["mySQL"]["user"]
        password = conf["mySQL"]["password"]
    except Exception:
        startLog.error("database information missing", console=True)
    else:
        startLog.proceed("database information found", console=True)

    # database connection check
    try:
        cnx = connect.connect()
        cursor = cnx.cursor()
    except exceptions.dbConnectionFail:
        startLog.error("unable to connect to database", console=True)
        return False
    else:
        cursor.close()
        cnx.close()
        startLog.proceed("database connected", console=True)

    # database table check and creation
    dbTables = ["prefix", "ignore", "cogs_list", "cogs_guild", "config", "channel", "archive", "leaderboard"]
    for table in dbTables:
        try:
            q = f"""SELECT * 
                    FROM information_schema.tables
                    WHERE table_schema = %s 
                    AND table_name = %s 
                    LIMIT %s;"""
            values = (database, table, 1)
            qData = query.queryV(q, values)

            if len(qData) == 0:
                if table == "prefix":
                    try:
                        tables.prefix()
                    except exceptions.dbTableCreationFail:
                        startLog.error("Unable to create 'prefix' db table or table already exists", console=True)
                        return False
                elif table == "ignore":
                    try:
                        tables.ignore()
                    except exceptions.dbTableCreationFail:
                        startLog.error("Unable to create 'ignore' db table or table already exists", console=True)
                        return False
                elif table == "cogs_list":
                    try:
                        tables.cogsList()
                    except exceptions.dbTableCreationFail:
                        startLog.error("Unable to create 'cogs_list' db table or table already exists", console=True)
                        return False
                elif table == "cogs_guild":
                    try:
                        tables.cogsGuild()
                    except exceptions.dbTableCreationFail:
                        startLog.error("Unable to create 'cogs_guild' db table or table already exists", console=True)
                        return False
                elif table == "config":
                    try:
                        tables.config()
                    except exceptions.dbTableCreationFail:
                        startLog.error("Unable to create 'config' db table or table already exists", console=True)
                        return False
                elif table == "channel":
                    try:
                        tables.channel()
                    except exceptions.dbTableCreationFail:
                        startLog.error("Unable to create 'channel' db table or table already exists", console=True)
                        return False
                elif table == "archive":
                    try:
                        tables.archive()
                    except exceptions.dbTableCreationFail:
                        startLog.error("Unable to create 'archive' db table or table already exists", console=True)
                        return False
                elif table == "leaderboard":
                    try:
                        tables.leaderboard()
                    except exceptions.dbTableCreationFail:
                        startLog.error("Unable to create 'leaderboard' db table or table already exists", console=True)
                        return False
                startLog.info(f"'{table}' db table created", console=True)
            else:
                startLog.proceed(f"{table} found", console=True)  
        except Exception:
            startLog.error("db checking failed", console=True)
            return False      