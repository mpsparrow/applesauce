'''
Checks if everything is allowed before running a command
'''
import discord
from discord.ext import commands
from utils import config, logger
import json

# checks if user is ignored in guild
def ignoredCheck(ctx, guildID):
    try: 
        conf = config.configLoad('guildconfig.json')
        ignoredUsers = conf[guildID]['ignored'] # gets ignored users

        if str(ctx.author) not in ignoredUsers: # if user is not in ignored users
            return True
        return False
    except:
        try: 
            conf[guildID]['ignored'] = []
            config.configDump('guildconfig.json', conf)
            return False
        except:
            logger.warningLog('Command Check Failure (ignored user)') # if accessing failed
            return False

# checks if command is disabled in guild
def guildCheck(ctx, guildID, name):
    try:
        conf = config.configLoad('guildconfig.json')
        return conf[guildID]["Commands"][name] # sees if it can access the required data
    except:
        guildBuild(ctx, guildID, name)
        return False

# checks and builds config file if fields are missing
def guildBuild(ctx, guildID, name):
    try:
        conf = config.configLoad('guildconfig.json')
        try:
            tmp1 = conf[guildID]
        except:
            conf1 = config.configLoad('guildconfig.json')
            conf1[guildID] = {}
            config.configDump('guildconfig.json', conf1)

        try:
            tmp2 = conf[guildID]["Commands"]
        except:
            conf2 = config.configLoad('guildconfig.json')
            conf2[guildID]["Commands"] = {}
            config.configDump('guildconfig.json', conf2)

        try:
            tmp4 = conf[guildID]["Commands"][name]
        except:
            conf3 = config.configLoad('guildconfig.json')
            conf3[guildID]["Commands"][name] = False
            config.configDump('guildconfig.json', conf3)
    except:
        logger.warningLog('Command Check Failure (rebuild)')

# main command check function
def isAllowed(ctx):
    try:
        # gets information about command
        conf = config.configLoad('guildconfig.json')
        guildID = str(ctx.guild.id)
        name = str(ctx.command.qualified_name)
    except:
        logger.warningLog('Command Check Failure (main)')
        return False

    return guildCheck(ctx, guildID, name) and ignoredCheck(ctx, guildID) # if all checks are passed