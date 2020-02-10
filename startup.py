'''
Bot Name: Applesauce
Created By: Matthew
Framework Version: v1.2.1
Last Updated: February 10, 2020
Created On: October 12, 2019

Please read license.txt for license information
'''
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
from utils import config, startupchecks, commandchecks, logger, dbQuery, dbConnect
import sys
import os
import datetime
import time

# gets prefix for bot
def get_prefix(bot, message): 
    return dbQuery.prefix(message.guild.id) # returns prefix

conf = config.read('mainConfig.ini') # loads config
botName = conf['main']['botname'] # gets bots name from config
bot = commands.Bot(command_prefix = get_prefix, case_insensitive = True) # gets bots prefix and case_insensitivity

# startupLog (command)
@bot.command(name='startupLog', description='prints startup-log.txt', usage='outputLog', aliases=['outlog', 'output', 'oplog', 'log'])
@commands.is_owner()
async def startupLog(ctx):
    await ctx.send(f"```{logger.output('startup-log.txt')}```") # sends startup-log.txt

# on startup
@bot.event
async def on_ready():
    startTime = time.time()

    logger.wipe('startup-log.txt')
    logger.wipe('runtime-log.txt')
    logger.infoStart('Running Checks')

    if startupchecks.startUpChecks() == False: # runs startup checks that are in startupchecks.py
        # if startup checks fail
        logger.errorStart("Something isn't configured correctly for startup")
        logger.errorStart("Startup aborted")
    else:
        # startup checks passed
        # writes startup information to startup-log.txt
        logger.write('startup-log.txt', f'Starting {botName}', "[info]", "\n")
        logger.infoStart(f'discord.py {discord.__version__}') # discord.py version
        logger.infoStart(f'Python {sys.version[:6]}') # python version

        # Requires Addons loading
        # Any file in /cogs/required is considered a required cog
        # These files MUST all be loaded in order for the bot to continue initializing
        logger.write('startup-log.txt', 'Initializing Required Cogs', "[info]", "\n")
        for required in os.listdir('./cogs/required'): # looks in /cogs/required
            if required.endswith('.py'): # if a .py file is found
                try:
                    bot.load_extension(f'cogs.required.{required[:-3]}') # loads cog
                    logger.passStart(f'{required} --> Success')
                except Exception as e:
                    logger.errorStart(f'{required} --> Failed')
                    logger.errorStart(f'{e}')
                    logger.errorStart('Startup aborted')
                    return

        # Main loading
        # Any file in /cogs/main is considered a cog
        # These files are attempted to be loaded. If a file errors then it is skipped and initializing continues
        logger.write('startup-log.txt', 'Initializing Cogs', "[info]", "\n")
        countSuccess = 0 
        countFail = 0
        countSkip = 0
        for cog in os.listdir(f'./cogs/main'): # looks in /cogs/main
            if cog.endswith('.py'): # if a .py file is found
                try:
                    value = dbQuery.cog(cog[:-3])
                    if value != True and value != False:
                        dbConnect.cogs(cog[:-3], False)
                        value = False
                except:
                    value = False
                    pass

                if value == True: # if module doesn't exist in excludedModules list (config.json)
                    try:
                        bot.load_extension(f'cogs.main.{cog[:-3]}') # load cog
                        logger.passStart(f'{cog} --> Success')
                        countSuccess += 1 # adds to successfully loaded cogs
                    except Exception as e:
                        logger.errorStart(f'{cog} --> Failed')
                        logger.errorStart(f'{e}')
                        countFail += 1 # adds to failed to load addons
                else:
                    logger.passStart(f'{cog} --> Skipped')
                    countSkip += 1 # adds to skipped cogs

        logger.infoStart(f'Success: {countSuccess}  Failed: {countFail}  Skipped: {countSkip}\n')
        logger.infoStart(f'{botName} is ready to rumble!')
        logger.infoStart(f'Initialized in {int((time.time() - startTime)*1000)}ms')

bot.run(conf['main']['discordToken']) # starts bot with Discord token from mainConfig.ini