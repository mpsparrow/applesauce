# Checks that are run at startup
# If any fail startup is aborted
from util import config, logger, dbConnect


def startUpChecks():
    # mainConfig.ini exists
    try:
        conf = config.readINI('mainConfig.ini')
        logger.passStart('mainConfig.ini found')
    except Exception as e:
        logger.errorStart('mainConfig.ini missing or unable to load')
        logger.errorStart(e)
        return False

    # database connection
    try:
        if dbConnect.connect() != False:
            logger.passStart('database connected')
        else:
            logger.errorStart('unable to connect to database')
            return False
    except Exception as e:
        logger.errorStart('unable to connect to database')
        logger.errorStart(e)
        return False

    # botname in mainConfig.ini
    try:
        name = conf['main']['botname']
        logger.passStart('botName found')
    except Exception as e:
        logger.errorStart('botname not found in mainConfig.ini')
        logger.errorStart(e)
        return False

    # default prefix in mainConfig.ini
    try:
        prefix = conf['main']['prefix']
        logger.passStart('prefix found')
    except Exception as e:
        logger.errorStart('prefix not found in mainConfig.ini')
        logger.errorStart(e)
        return False

    # token in mainConfig.ini
    try:
        token = conf['main']['discordToken']
        logger.passStart('token found')
    except Exception as e:
        logger.errorStart('token not found in mainConfig.ini')
        logger.errorStart(e)
        return False
    return True