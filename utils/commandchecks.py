'''
Checks if everything is allowed before running a command
'''
import discord
from discord.ext import commands
from utils import config, logger, dbQuery
import json

# checks if user is ignored in guild
def ignoredCheck(ctx, guildID):
    try: 
        return not(dbQuery.ignore(guildID, ctx.message.author.id))
    except Exception as e:
        logger.warnRun('Command Check Failure (ignored user)') # if accessing failed
        logger.normRun(e)
        return True

# checks if command is disabled in guild
def guildCheck(ctx, guildID, name):
    try:
        conf = config.readJSON('guildconfig.json')
        return conf[guildID]["Commands"][name] # sees if it can access the required data
    except:
        guildBuild(ctx, guildID, name)
        return False

# checks and builds config file if fields are missing
def guildBuild(ctx, guildID, name):
    try:
        conf = config.readJSON('guildconfig.json')
        try:
            tmp1 = conf[guildID]
        except:
            conf1 = config.readJSON('guildconfig.json')
            conf1[guildID] = {}
            config.dumpJSON('guildconfig.json', conf1)

        try:
            tmp2 = conf[guildID]["Commands"]
        except:
            conf2 = config.readJSON('guildconfig.json')
            conf2[guildID]["Commands"] = {}
            config.dumpJSON('guildconfig.json', conf2)

        try:
            tmp4 = conf[guildID]["Commands"][name]
        except:
            conf3 = config.readJSON('guildconfig.json')
            conf3[guildID]["Commands"][name] = False
            config.dumpJSON('guildconfig.json', conf3)
    except:
        logger.warnRun('Command Check Failure (rebuild)')

# main command check function
def isAllowed(ctx):
    try:
        # gets information about command
        conf = config.readJSON('guildconfig.json')
        guildID = str(ctx.guild.id)
        name = str(ctx.command.qualified_name)
    except:
        logger.warnRun('Command Check Failure (main)')
        return False

    return guildCheck(ctx, guildID, name) and ignoredCheck(ctx, guildID) # if all checks are passed