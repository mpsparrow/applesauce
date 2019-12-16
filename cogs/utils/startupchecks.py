from . import configloader, logger
import json

def startUpChecks():
    # checks config.json for important missing information
    try:
        config = configloader.configLoad('config.json')
        logger.outputWrite(' config.json successfully loaded')
    except:
        logger.outputWrite(' config.json missing or unable to load')
        return False
    
    try:
        config2 = configloader.configLoad('guildconfig.json')
        logger.outputWrite(' guildconfig.json successfully loaded')
    except:
        logger.outputWrite(' guildconfig.json missing or unable to load')
        return False

    try:
        name = config['main']['botName']
        logger.outputWrite(' botName found')
    except:
        logger.outputWrite(' failed to retrieve botName from config.json')
        return False

    try:
        prefix = config['main']['prefix']
        logger.outputWrite(' prefix found')
    except:
        logger.outputWrite(' failed to retrieve prefix from config.json')
        return False

    try:
        token = config['main']['token']
        logger.outputWrite(' token found')
    except:
        logger.outputWrite(' failed to retrieve token from config.json')
        return False
    return True