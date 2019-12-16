import discord
from discord.ext import commands
from . import configloader, logger
import json

# checks if user is ignored in guild
def ignoredCheck(ctx, guildID):
    try: 
        config = configloader.configLoad('guildconfig.json')
        ignoredUsers = config[guildID]['ignored'] # gets ignored users

        if str(ctx.author) not in ignoredUsers: # if user is not in ignored users
            return True
        return False
    except:
        try: 
            config[guildID]['ignored'] = []
            configloader.configDump('guildconfig.json', config)
            return False
        except:
            logger.logWrite('output-log.txt', f'Command Check Failure (ignored user)') # if accessing failed
            return False

# checks if command is disabled in guild
def guildCheck(ctx, guildID, name):
    try:
        config = configloader.configLoad('guildconfig.json')
        return config[guildID]["Commands"][name] # sees if it can access the required data
    except:
        guildBuild(ctx, guildID, name)
        return False

# checks and builds config file if fields are missing
def guildBuild(ctx, guildID, name):
    try:
        config = configloader.configLoad('guildconfig.json')
        try:
            tmp1 = config[guildID]
        except:
            config1 = configloader.configLoad('guildconfig.json')
            config1[guildID] = {}
            configloader.configDump('guildconfig.json', config1)
    
        try:
            tmp2 = config[guildID]["Commands"]
        except:
            config2 = configloader.configLoad('guildconfig.json')
            config2[guildID]["Commands"] = {}
            configloader.configDump('guildconfig.json', config2)
        
        try:
            tmp4 = config[guildID]["Commands"][name]
        except:
            config3 = configloader.configLoad('guildconfig.json')
            config3[guildID]["Commands"][name] = False
            configloader.configDump('guildconfig.json', config3)
    except:
        logger.logWrite('output-log.txt', 'Command Check Failure (rebuild)')

# main command check function
def isAllowed(ctx):
    try:
        # gets information about command
        config = configloader.configLoad('guildconfig.json')
        guildID = str(ctx.guild.id)
        name = str(ctx.command.qualified_name)
    except:
        logger.logWrite('output-log.txt', 'Command Check Failure (main)')
        return False

    return guildCheck(ctx, guildID, name) and ignoredCheck(ctx, guildID) # if all checks are passed