'''
Applesauce
Created By: Matthew
Framework Version: v1.2
Last Updated: December 14, 2019
Created On: October 12, 2019

Please read license.txt for license information.
'''

import discord
from discord.ext import commands
from cogs.utils import configloader, startupchecks, commandchecks, databaseconnect
from discord.ext.commands import has_permissions
from logs import logger
import sys
import os
import datetime
import json

# gets prefix
def get_prefix(bot, message): 
    try:
        configGuild = configloader.configLoad('guildconfig.json') # loads guildconfig.json
        return configGuild[str(message.guild.id)]['prefix'] # returns guild specific prefix
    except:
        config = configloader.configLoad('config.json') # loads config.json
        return config['main']['prefix'] # returns default prefix if no guild prefix is found

config = configloader.configLoad('config.json') # loads config.json
botName = config['main']['botName'] # gets bots name from config.json
bot = commands.Bot(command_prefix = get_prefix, case_insensitive = True) # gets bots prefix and case_insensitivity

# output log command
@bot.command(name="outputLog", description="prints output log", usage="outputLog")
@commands.is_owner()
async def outputLog(ctx):
    with open(r'logs/output-log.txt') as f: # opens log file
        await ctx.send(f"```{f.read()}```") # sends log file in message

@bot.event
async def on_ready(): # on startup
    ### clears logs
    logger.outputWipe() # output-log.txt
    logger.messageWipe() # message-log.txt
    logger.commandWipe() # command-log.txt

    logger.outputWrite('Running Checks')
    if startupchecks.startUpChecks() == False: # runs startup checks in startupchecks.py
        ### if startup checks fail
        logger.outputWipe() # create and clear output-log.txt
        logger.outputWrite(f"Something isn't configured correctly for Applesauce to startup.") # output-log.txt
        logger.outputWrite(f"Startup aborted")
    else:
        ### startup checks passed
        ### writes startup info to output-log.txt
        logger.outputWrite(f' Passed Checks\n')
        logger.outputWrite(f'Starting {botName}\n')
        logger.outputWrite('Debug:')
        logger.outputWrite(f' date/time: {datetime.datetime.now()}') # date and time
        logger.outputWrite(f' discord.py version: {discord.__version__}') # discord.py version
        logger.outputWrite(f' python version: {sys.version}') # python version

        ### Requires Addons loading
        ### Any file in /cogs/required is considered a required cog.
        ### These files MUST all be loaded in order for the bot to continue initializing.
        logger.outputWrite('\nInitializing Required Extensions') # output-log.txt
        for required in os.listdir('./cogs/required'): # looks in /cogs/required
            if required.endswith('.py'): # if a .py file is found
                if required[:-3] not in config['main']['excludedRequired']: # checks if config lists required cog as excluded
                    try:
                        bot.load_extension(f'cogs.required.{required[:-3]}') # load file
                        logger.outputWrite(f' Successfully loaded {required}') # output-log.txt
                    except Exception as e:
                        logger.outputWrite(f' Failed to load {required} (required cog)') # output-log.txt
                        logger.outputWrite(f' {e}') # output-log.txt
                        logger.outputWrite('Startup aborted') # output-log.txt
                        return

        ### Main loading
        ### Any file in /cogs/main is considered a cog.
        ### These files are attempted to be loaded. If a file errors then it is skipped and initializing continues.
        logger.outputWrite('\nInitializing Cogs') # output-log.txt
        countSuccess = 0 # counts cogs that successful loaded (not including required addons)
        countFail = 0 # counts cogs that failed to load (not including required addons)
        countSkip = 0 # counts cogs that were skipped from loading (not including required addons)
        for cog in os.listdir(f'./cogs/main'): # looks in /cogs/main
            if cog.endswith('.py'): # if a .py file is found
                try:
                    value = config['cogs'][cog[:-3]]
                except:
                    newConfig = configloader.configLoad('config.json')
                    newConfig['cogs'][cog[:-3]] = False
                    configloader.configDump('config.json', newConfig)
                    value = False

                if value == True: # if module doesn't exist in excludedModules list (config.json)
                    try:
                        bot.load_extension(f'cogs.main.{cog[:-3]}') # load cog
                        logger.outputWrite(f' Successfully loaded {cog}') # output-log.txt
                        countSuccess += 1 # adds to successfully loaded cogs
                    except Exception as e:
                        logger.outputWrite(f' Failed to load {cog}') # output-log.txt
                        logger.outputWrite(f'  Error: {e}') # output-log.txt
                        countFail += 1 # adds to failed to load addons
                else:
                    logger.outputWrite(f' Skipped loading {cog}') # output-log.txt
                    countSkip += 1 # adds to skipped cogs

        logger.outputWrite(f' Cogs Loaded: Success: {countSuccess}  Failed: {countFail}  Skipped: {countSkip}\n') # output-log.txt
        logger.outputWrite(f'{botName} is ready to rumble!') # output-log.txt

bot.run(config['main']['token']) # gets Discord token from config.json and starts bot