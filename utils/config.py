'''
Useful functions to retrieve and load config information
'''
import json

# config loader
def configLoad(filename):
    with open(filename, 'r') as jsondata:
        f = json.load(jsondata)
    return f

# config dumper
def configDump(filename, data):
    with open(filename, 'w') as jsondata:
        json.dump(data, jsondata, indent=4)

# get prefix
def guildPrefix(guildid):
    try:
        conf = configLoad('guildconfig.json')
        prefix = conf[guildid]['prefix']
    except:
        conf = configLoad('config.json')
        prefix = conf2['main']['prefix']
    return prefix