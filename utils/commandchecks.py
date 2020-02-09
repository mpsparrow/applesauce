'''
Checks if everything is allowed before running a command
'''
import discord
from discord.ext import commands
from utils import config, logger, dbQuery, dbConnect
import json

# checks if user is ignored in guild
def ignoredCheck(ctx, guildID):
    try: 
        return not(dbQuery.ignore(guildID, ctx.message.author.id))
    except Exception as e:
        logger.errorRun("commandchecks.py ignoredCheck - command check failure")
        logger.normRun(e)
        return False

# checks if command is disabled in guild
def guildCheck(ctx, guildID, name):
    try:
        return dbQuery.command(guildID, str(name))
    except Exception as e:
        logger.errorRun("commandchecks.py guildCheck - command check failure")
        logger.normRun(e)
        return False

# main command check function
def isAllowed(ctx):
    try:
        # gets information about command
        guildID = str(ctx.guild.id)
        name = str(ctx.command.qualified_name)
        value =  guildCheck(ctx, guildID, name) and ignoredCheck(ctx, guildID) # if all checks are passed
        if value:
            dbConnect.commandCount(guildID, name)
        return value
    except Exception as e:
        logger.errorRun("commandchecks.py isAllowed - command check failure")
        logger.normRun(e)
        return False