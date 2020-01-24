'''
Bot Name: Applesauce
Created By: Matthew
Framework Version: v1.2.3
Last Updated: January 24, 2020
Created On: October 12, 2019

Please read license.txt for license information
'''
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
from utils import config, startupchecks, commandchecks, logger
import sys
import os
import datetime
import time
import json

# gets prefix for bot
def get_prefix(bot, message): 
    return config.guildPrefix(str(message.guild.id)) # returns prefix

conf = config.configLoad('config.json') # loads config
botName = conf['main']['botName'] # gets bots name from config
bot = commands.Bot(command_prefix = get_prefix, case_insensitive = True) # gets bots prefix and case_insensitivity

# outputLog (command)
@bot.command(name='outputLog', description='prints output-log.txt', usage='outputLog')
@commands.is_owner()
async def outputLog(ctx):
    await ctx.send(f"```{logger.logReturn('output-log.txt')}```") # sends output-log.txt

# on startup
@bot.event
async def on_ready():
    startTime = time.time()
    # await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="started"))

    logger.logWipe('output-log.txt')
    logger.infoLog('Running Checks')

    if startupchecks.startUpChecks() == False: # runs startup checks that are in startupchecks.py
        # if startup checks fail
        logger.errorLog("Something isn't configured correctly for Applesauce to startup.")
        logger.errorLog("Startup aborted")
    else:
        # startup checks passed
        # writes startup information to output-log.txt
        logger.logWrite('output-log.txt', f'Starting {botName}', "[info]", "\n")
        logger.infoLog(f'discord.py {discord.__version__}') # discord.py version
        logger.infoLog(f'Python {sys.version[:6]}') # python version

        # Requires Addons loading
        # Any file in /cogs/required is considered a required cog
        # These files MUST all be loaded in order for the bot to continue initializing
        logger.logWrite('output-log.txt', 'Initializing Required Cogs', "[info]", "\n")
        for required in os.listdir('./cogs/required'): # looks in /cogs/required
            if required.endswith('.py'): # if a .py file is found
                if required[:-3] not in conf['main']['excludedRequired']: # checks if config lists required cog as excluded
                    try:
                        bot.load_extension(f'cogs.required.{required[:-3]}') # loads cog
                        logger.passedLog(f'{required} --> Success')
                    except Exception as e:
                        logger.errorLog(f'{required} --> Failed')
                        logger.errorLog(f'{e}')
                        logger.errorLog('Startup aborted')
                        return

        # Main loading
        # Any file in /cogs/main is considered a cog
        # These files are attempted to be loaded. If a file errors then it is skipped and initializing continues
        logger.logWrite('output-log.txt', 'Initializing Cogs', "[info]", "\n")
        countSuccess = 0 
        countFail = 0
        countSkip = 0
        for cog in os.listdir(f'./cogs/main'): # looks in /cogs/main
            if cog.endswith('.py'): # if a .py file is found
                try:
                    value = conf['cogs'][cog[:-3]]
                except:
                    newConfig = config.configLoad('config.json')
                    newConfig['cogs'][cog[:-3]] = False
                    config.configDump('config.json', newConfig)
                    value = False

                if value == True: # if module doesn't exist in excludedModules list (config.json)
                    try:
                        bot.load_extension(f'cogs.main.{cog[:-3]}') # load cog
                        logger.passedLog(f'{cog} --> Success')
                        countSuccess += 1 # adds to successfully loaded cogs
                    except Exception as e:
                        logger.errorLog(f'{cog} --> Failed')
                        logger.errorLog(f'{e}')
                        countFail += 1 # adds to failed to load addons
                else:
                    logger.passedLog(f'{cog} --> Skipped')
                    countSkip += 1 # adds to skipped cogs

        logger.infoLog(f'Success: {countSuccess}  Failed: {countFail}  Skipped: {countSkip}\n')
        logger.infoLog(f'{botName} is ready to rumble!')
        logger.infoLog(f'Initialized in {int((time.time() - startTime)*1000)}ms')

bot.run(conf['main']['token']) # gets Discord token from config.json and starts bot