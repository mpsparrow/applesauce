'''
Useful functions to get config information
'''
from . import configloader

def guildPrefix(guildid):
    try:
        config = configloader.configLoad('guildconfig.json')
        prefix = config[guildid]['prefix']
    except:
        config = configloader.configLoad('config.json')
        prefix = config2['main']['prefix']
    return prefix