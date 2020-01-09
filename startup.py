'''
Applesauce
Created By: Matthew
Framework Version: v1.2
Last Updated: January 8, 2020
Created On: October 12, 2019

Please read license.txt for license information
'''
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
from cogs.utils import configloader, startupchecks, commandchecks, databaseconnect, logger
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

# outputLog command
@bot.command(name='outputLog', description='prints output-log.txt', usage='outputLog')
@commands.is_owner()
async def outputLog(ctx):
    await ctx.send(f"```{logger.logReturn('output-log.txt')}```") # sends output-log.txt file in message

# on startup
@bot.event
async def on_ready():
    logger.logWipe('output-log.txt')
    logger.logWrite('output-log.txt', 'Running Checks')

    if startupchecks.startUpChecks() == False: # runs startup checks that are in startupchecks.py
        # if startup checks fail
        logger.logWrite('output-log.txt', f"Something isn't configured correctly for Applesauce to startup.", '[error]')
        logger.logWrite('output-log.txt', f"Startup aborted", '[error]')
    else:
        # startup checks passed
        # writes startup information to output-log.txt
        logger.logWrite('output-log.txt', f'Passed Checks\n')
        logger.logWrite('output-log.txt', f'Starting {botName}\n')
        logger.logWrite('output-log.txt', 'Getting Debug Information')
        logger.logWrite('output-log.txt', f'discord.py {discord.__version__}') # discord.py version
        logger.logWrite('output-log.txt', f'Python {sys.version[:6]}') # python version

        # Requires Addons loading
        # Any file in /cogs/required is considered a required cog
        # These files MUST all be loaded in order for the bot to continue initializing
        logger.logWrite('output-log.txt', 'Initializing Required Cogs', "", "\n")
        for required in os.listdir('./cogs/required'): # looks in /cogs/required
            if required.endswith('.py'): # if a .py file is found
                if required[:-3] not in config['main']['excludedRequired']: # checks if config lists required cog as excluded
                    try:
                        bot.load_extension(f'cogs.required.{required[:-3]}') # loads cog
                        logger.logWrite('output-log.txt', f'{required} --> Success')
                    except Exception as e:
                        logger.logWrite('output-log.txt', f'{required} --> Failed', '[error]')
                        logger.logWrite('output-log.txt', f'{e}', '[error]')
                        logger.logWrite('output-log.txt', 'Startup aborted', '[error]')
                        return

        # Main loading
        # Any file in /cogs/main is considered a cog
        # These files are attempted to be loaded. If a file errors then it is skipped and initializing continues
        logger.logWrite('output-log.txt', 'Initializing Cogs', "", "\n")
        countSuccess = 0 
        countFail = 0
        countSkip = 0
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
                        logger.logWrite('output-log.txt', f'{cog} --> Success')
                        countSuccess += 1 # adds to successfully loaded cogs
                    except Exception as e:
                        logger.logWrite('output-log.txt', f'{cog} --> Failed', '[error]')
                        logger.logWrite('output-log.txt', f' Error: {e}', '[error]')
                        countFail += 1 # adds to failed to load addons
                else:
                    logger.logWrite('output-log.txt', f'{cog} --> Skipped')
                    countSkip += 1 # adds to skipped cogs

        logger.logWrite('output-log.txt', f'Cogs Loaded: Success: {countSuccess}  Failed: {countFail}  Skipped: {countSkip}\n')
        logger.logWrite('output-log.txt', f'{botName} is ready to rumble!')

bot.run(config['main']['token']) # gets Discord token from config.json and starts bot