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
    Runs through pile of startup checks and returns True if they all pass.
    """

    # mainConfig.ini access check
    try:
        conf = config.readINI("mainConfig.ini")
        startLog.proceed("mainConfig.ini found", console=True)
    except exceptions.configReadError:
        startLog.error("mainConfig.ini missing or unable to load configReadError", console=True)
        return False

    # botname in mainConfig.ini
    try:
        name = conf["main"]["botname"]
    except:
        startLog.error("botname not found in mainConfig.ini", console=True)
        return False
    else:
        startLog.proceed("botName found", console=True)

    # default prefix in mainConfig.ini
    try:
        prefix = conf["main"]["prefix"]
    except:
        startLog.error("prefix not found in mainConfig.ini", console=True)
        return False
    else:
        startLog.proceed("botName found", console=True)

    # token in mainConfig.ini
    try:
        prefix = conf["main"]["discordToken"]
    except:
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
    except:
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
    dbTables = ["prefix", "ignore", "commands", "cogs", "config", "archive", "leaderboard"]
    for table in dbTables:
        try:
            q = f"""SELECT * 
                    FROM information_schema.tables
                    WHERE table_schema = %s 
                    AND table_name = %s 
                    LIMIT 1;"""
            values = (database, table)
            qData = query.queryV(q, values)

            if len(qData) == 0:
                if table == "prefix":
                    try:
                        tables.prefix()
                    except exceptions.dbTableCreationFail:
                        startLog.error("Unable to create 'prefix' db table or table already exists. dbTableCreationFail (tables.prefix)", console=True)
                        return False
                elif table == "ignore":
                    try:
                        tables.ignore()
                    except exceptions.dbTableCreationFail:
                        startLog.error("Unable to create 'ignore' db table or table already exists. dbTableCreationFail (tables.ignore)", console=True)
                        return False
                elif table == "commands":
                    try:
                        tables.commands()
                    except exceptions.dbTableCreationFail:
                        startLog.error("Unable to create 'commands' db table or table already exists. dbTableCreationFail (tables.commands)", console=True)
                        return False
                elif table == "cogs":
                    try:
                        tables.cogs()
                    except exceptions.dbTableCreationFail:
                        startLog.error("Unable to create 'cogs' db table or table already exists. dbTableCreationFail (tables.cogs)", console=True)
                        return False
                elif table == "config":
                    try:
                        tables.config()
                    except exceptions.dbTableCreationFail:
                        startLog.error("Unable to create 'config' db table or table already exists. dbTableCreationFail (tables.config)", console=True)
                        return False
                elif table == "archive":
                    try:
                        tables.archive()
                    except exceptions.dbTableCreationFail:
                        startLog.error("Unable to create 'archive' db table or table already exists. dbTableCreationFail (tables.archive)", console=True)
                        return False
                elif table == "leaderboard":
                    try:
                        tables.leaderboard()
                    except exceptions.dbTableCreationFail:
                        startLog.error("Unable to create 'leaderboard' db table or table already exists. dbTableCreationFail (tables.leaderboard)", console=True)
                        return False
                startLog.info(f"'{table}' db table created", console=True)
            else: 
                startLog.proceed(f"{table} found", console=True)  
        except:
            startLog.error("db checking failed", console=True)
            return False      