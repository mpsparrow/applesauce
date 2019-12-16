from . import configloader, logger
import json

def startUpChecks():
    # checks config.json for important missing information
    try:
        config = configloader.configLoad('config.json')
        logger.logWrite('output-log.txt', ' config.json successfully loaded')
    except:
        logger.logWrite('output-log.txt', ' config.json missing or unable to load')
        return False
    
    try:
        config2 = configloader.configLoad('guildconfig.json')
        logger.logWrite('output-log.txt', ' guildconfig.json successfully loaded')
    except:
        logger.logWrite('output-log.txt', ' guildconfig.json missing or unable to load')
        return False

    try:
        name = config['main']['botName']
        logger.logWrite('output-log.txt', ' botName found')
    except:
        logger.logWrite('output-log.txt', ' failed to retrieve botName from config.json')
        return False

    try:
        prefix = config['main']['prefix']
        logger.logWrite('output-log.txt', ' prefix found')
    except:
        logger.logWrite('output-log.txt', ' failed to retrieve prefix from config.json')
        return False

    try:
        token = config['main']['token']
        logger.logWrite('output-log.txt', ' token found')
    except:
        logger.logWrite('output-log.txt', ' failed to retrieve token from config.json')
        return False
    return True