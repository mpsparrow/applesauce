'''
Applesauce
Created By: Matthew
Framework Version: v1.0
Last Updated: November 16, 2019
Created On: October 12, 2019

Please read LICENSE.txt for license information.
'''

import discord
from discord.ext import commands
from cogs.utils import configloader
from cogs.utils import startupchecks
from logs import logger
import sys
import os
import datetime
import json


botName = configloader.config['main']['botName'] # gets bots name from config.json
bot = commands.Bot(command_prefix = configloader.config['main']['prefix'], case_insensitive = True) # gets bots prefix from config.json

@bot.event
async def on_ready():
    if startupchecks.startUpChecks() == True:
        # clears logs
        logger.outputWipe() # output-log.txt
        logger.messageWipe() # message-log.txt
        logger.commandWipe() # command-log.txt

        # writes startup info to output-log.txt
        logger.outputWrite(f'Starting {botName}')
        logger.outputWrite('Debug:')
        logger.outputWrite(f' date/time: {datetime.datetime.now()}') # date and time
        logger.outputWrite(f' discord.py version: {discord.__version__}') # discord py version
        logger.outputWrite(f' python version: {sys.version}\n') # python version
        logger.outputWrite(f'Passed Checks')

        # Requires Addons loading
        # Any file in /cogs/required is considered a required addons.
        # These files MUST all be loaded in order for the bot to continue initializing.
        logger.outputWrite('\nInitializing Required Extensions') # output-log.txt
        for required in os.listdir('./cogs/required'): # looks in /cogs/required
            if required.endswith('.py'): # if a .py file is found
                if required[:-3] not in configloader.config['main']['excludedRequired']:
                    try:
                        bot.load_extension(f'cogs.required.{required[:-3]}') # load file
                        logger.outputWrite(f' Successfully loaded {required}') # output-log.txt
                    except Exception as e:
                        logger.outputWrite(f' Failed to load {required}') # output-log.txt
                        logger.outputWrite(f' {e}') # output-log.txt
                        logger.outputWrite('startup aborted') # output-log.txt
                        return

        # Addons loading
        # Any file in /cogs/addons is considered an addon.
        # These files are attempted to be loaded. If a file fails/errors then it is skipped and initializing continues.
        logger.outputWrite('\nInitializing Addons') # output-log.txt
        countSuccess = 0 # counts addons that successful loaded (not including required addons)
        countFail = 0 # counts addons that failed to load (not including required addons)
        countSkip = 0 # counts addons that were skipped from loading (not including required addons)
        for folder in configloader.config['main']['subfolders']:
            for addons in os.listdir(f'./cogs/addons/{folder}'): # looks in /cogs/addons
                if addons.endswith('.py'): # if a .py file is found
                    try:
                        value = configloader.config['addons'][addons[:-3]]
                    except:
                        with open(r'config.json', 'r') as file:
                            json_data = json.load(file)
                            json_data['addons'][addons[:-3]] = False
                        with open(r'config.json', 'w') as file:
                            json.dump(json_data, file, indent=2)
                        value = False

                    if value == True: # if module doesn't exist in excludedModules list (config.json)
                        try:
                            bot.load_extension(f'cogs.addons.{folder}.{addons[:-3]}') # load addon
                            logger.outputWrite(f' Successfully loaded {folder}/{addons}') # output-log.txt
                            countSuccess += 1 # adds to successfully loaded addons
                        except Exception as e:
                            logger.outputWrite(f' Failed to load {folder}/{addons}') # output-log.txt
                            logger.outputWrite(f'  Error: {e}') # output-log.txt
                            countFail += 1 # adds to failed to load addons
                    else:
                        logger.outputWrite(f' Skipped loading {folder}/{addons}') # output-log.txt
                        countSkip += 1 # adds to skipped addons

        logger.outputWrite(f' Addons Loaded: Success: {countSuccess}  Failed: {countFail}  Skipped: {countSkip}\n') # output-log.txt
        logger.outputWrite(f'{botName} is ready to rumble!') # output-log.txt
    else:
        logger.outputWipe() # create and clear output-log.txt
        logger.outputWrite(f"Something isn't configured correctly for Applesauce to startup. Please check config.json") # output-log.txt

bot.run(configloader.config['main']['token']) # gets Discord token from config.json and starts bot
