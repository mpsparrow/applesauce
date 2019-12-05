import discord
from discord.ext import commands
from logs import logger
from . import configloader
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
            logger.outputWrite(f'Command Check Failure (ignored user)') # if accessing failed
            return False

# checks if command is disabled in guild
def guildCheck(ctx, guildID, cog, name):
    try:
        config = configloader.configLoad('guildconfig.json')
        return config[guildID]["Commands"][cog][name] # sees if it can access the required data
    except:
        guildBuild(ctx, guildID, cog, name)
        return False

# checks and builds config file if fields are missing
def guildBuild(ctx, guildID, cog, name):
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
            tmp3 = config[guildID]["Commands"][cog]
        except:
            config3 = configloader.configLoad('guildconfig.json')
            config3[guildID]["Commands"][cog] = {}
            configloader.configDump('guildconfig.json', config3)

        try:
            tmp4 = config[guildID]["Commands"][cog][name]
        except:
            config4 = configloader.configLoad('guildconfig.json')
            config4[guildID]["Commands"][cog][name] = False
            configloader.configDump('guildconfig.json', config4)
    except:
        logger.outputWrite('Command Check Failure (rebuild)')

# main command check function
def isAllowed(ctx):
    try:
        # gets information about command
        config = configloader.configLoad('guildconfig.json')
        guildID = str(ctx.guild.id)
        cog = str(ctx.command.cog.qualified_name)
        name = str(ctx.command.qualified_name)
    except:
        logger.outputWrite('Command Check Failure (main)')
        return False

    return guildCheck(ctx, guildID, cog, name) and ignoredCheck(ctx, guildID) # if all checks are passed