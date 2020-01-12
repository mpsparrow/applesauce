'''
Checks to run on bot startup
'''
from utils import config, logger
import json

def startUpChecks():
    # config.json loads
    try:
        conf = config.configLoad('config.json')
        logger.passedLog('config.json successfully loaded')
    except Exception as e:
        logger.errorLog('config.json missing or unable to load')
        logger.errorLog(f'{e}')
        return False
    
    # guildconfig.json loads
    try:
        conf2 = config.configLoad('guildconfig.json')
        logger.passedLog('guildconfig.json successfully loaded')
    except Exception as e:
        logger.errorLog('guildconfig.json missing or unable to load')
        logger.errorLog(f'{e}')
        return False

    # bot has a working name
    try:
        name = conf['main']['botName']
        logger.passedLog('botName found')
    except Exception as e:
        logger.errorLog('failed to retrieve botName from config.json')
        logger.errorLog(f'{e}')
        return False

    # bot has a default prefix
    try:
        prefix = conf['main']['prefix']
        logger.passedLog('prefix found')
    except Exception as e:
        logger.errorLog('failed to retrieve prefix from config.json')
        logger.errorLog(f'{e}')
        return False

    # bot has a token
    try:
        token = conf['main']['token']
        logger.passedLog('token found')
    except Exception as e:
        logger.errorLog('failed to retrieve token from config.json')
        logger.errorLog(f'{e}')
        return False
    return True