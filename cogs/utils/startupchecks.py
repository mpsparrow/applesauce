from . import configloader
import json

def startUpChecks():
    # checks config.json for important missing information
    try:
        config = configloader.configLoad('config.json')
        config2 = configloader.configLoad('guildconfig.json')
        name = config['main']['botName']
        prefix = config['main']['prefix']
        token = config['main']['token']
        addons = config['cogs']
        return True
    except:
        return False