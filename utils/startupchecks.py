'''
Checks to run on bot startup
'''
from utils import config, logger
import json

def startUpChecks():
    # mainConfig.ini loads
    try:
        conf = config.read('mainConfig.ini')
        logger.passStart('mainConfig.ini successfully loaded')
    except Exception as e:
        logger.errorStart('mainConfig.ini missing or unable to load')
        logger.errorStart(f'{e}')
        return False
    
    # guildconfig.json loads
    try:
        conf2 = config.readJSON('guildconfig.json')
        logger.passStart('guildconfig.json successfully loaded')
    except Exception as e:
        logger.errorStart('guildconfig.json missing or unable to load')
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