# Checks that are run at startup
# If any fail startup is aborted
import json
from util import config, logger

def startUpChecks():
    # mainConfig.ini loads
    try:
        conf = config.readINI('mainConfig.ini')
        logger.passStart('mainConfig.ini successfully loaded')
    except Exception as e:
        logger.errorStart('mainConfig.ini missing or unable to load')
        logger.errorStart(f'{e}')
        return False

    # checks for name
    try:
        name = conf['main']['botname']
        logger.passStart('botName found')
    except Exception as e:
        logger.errorStart('botname not found in mainConfig.ini')
        logger.errorStart(f'{e}')
        return False

    # checks for default prefix
    try:
        prefix = conf['main']['prefix']
        logger.passStart('prefix found')
    except Exception as e:
        logger.errorStart('prefix not found in mainConfig.ini')
        logger.errorStart(f'{e}')
        return False

    # checks for token
    try:
        token = conf['main']['discordToken']
        logger.passStart('token found')
    except Exception as e:
        logger.errorStart('token not found in mainConfig.ini')
        logger.errorStart(f'{e}')
        return False
    return True