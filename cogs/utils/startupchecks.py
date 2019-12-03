from . import configloader
import json

def startUpChecks():
    # checks config.json for important missing information
    try:
        name = configloader.config['main']['botName']
        prefix = configloader.config['main']['prefix']
        token = configloader.config['main']['token']
        addons = configloader.config['cogs']
        return True
    except:
        return False
