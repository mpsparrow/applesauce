"""
Checks to run through on startup of bot
"""
from util import config
from util.log import startLog
from util.db import query, tables, connect

def checks():
    """
    Runs through pile of startup checks and returns True if they all pass.
    """

    # mainConfig.ini access check
    try:
        conf = config.readINI("mainConfig.ini")
        startLog.proceed("mainConfig.ini found")
    except configReadError:
        startLog.error("mainConfig.ini missing or unable to load configReadError")
        return False

    # botname in mainConfig.ini
    try:
        name = conf["main"]["botname"]
    except:
        startLog.error("botname not found in mainConfig.ini")
        return False
    else:
        startLog.proceed("botName found")

    # default prefix in mainConfig.ini
    try:
        prefix = conf["main"]["prefix"]
    except:
        startLog.error("prefix not found in mainConfig.ini")
        return False
    else:
        startLog.proceed("botName found")

    # token in mainConfig.ini
    try:
        prefix = conf["main"]["discordToken"]
    except:
        startLog.error("token not found in mainConfig.ini")
        return False
    else:
        startLog.proceed("token found")

    # db information
    try:
        host = conf["mySQL"]["host"]
        database = conf["mySQL"]["database"]
        user = conf["mySQL"]["user"]
        password = conf["mySQL"]["password"]
    except:
        startLog.error("database information missing")
    else:
        startLog.proceed("")

    # database connection check
    try:
        cnx = connect.connect()
        cursor = cnx.cursor()
    except dbConnectionFail:
        startLog.error("unable to connect to database")
        return False
    else:
        cursor.close()
        cnx.close()
        startLog.proceed("database connected")

    # database table check and creation
    tables = ["prefix", "ignore", "commands", "cogs", "config", "archive", "leaderboard"]
    for table in tables:
        try:
            q = f"""SELECT * 
                    FROM information_schema.tables
                    WHERE table_schema = '{database}'
                    AND table_name = '{table}'
                    LIMIT 1;"""
            query.query(q)
        except dbQueryFail:
            if table == "prefix":
                try:
                    tables.prefix()
                except dbTableCreationFail:
                    startLog.error("Unable to create 'prefix' db table or table already exists. dbTableCreationFail (tables.prefix)")
                    return False
            elif table == "ignore":
                try:
                    tables.ignore()
                except dbTableCreationFail:
                    startLog.error("Unable to create 'ignore' db table or table already exists. dbTableCreationFail (tables.ignore)")
                    return False
            elif table == "commands":
                try:
                    tables.commands()
                except dbTableCreationFail:
                    startLog.error("Unable to create 'commands' db table or table already exists. dbTableCreationFail (tables.commands)")
                    return False
            elif table == "cogs":
                try:
                    tables.cogs()
                except dbTableCreationFail:
                    startLog.error("Unable to create 'cogs' db table or table already exists. dbTableCreationFail (tables.cogs)")
                    return False
            elif table == "config":
                try:
                    tables.config()
                except dbTableCreationFail:
                    startLog.error("Unable to create 'config' db table or table already exists. dbTableCreationFail (tables.config)")
                    return False
            elif table == "archive":
                try:
                    tables.archive()
                except dbTableCreationFail:
                    startLog.error("Unable to create 'archive' db table or table already exists. dbTableCreationFail (tables.archive)")
                    return False
            elif table == "leaderboard":
                try:
                    tables.leaderboard()
                except dbTableCreationFail:
                    startLog.error("Unable to create 'leaderboard' db table or table already exists. dbTableCreationFail (tables.leaderboard)")
                    return False
            startLog.info(f"'{table}' db table created")
        finally:
            startLog.proceed(f"{table} found")   