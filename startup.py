'''
Bot Name: Applesauce
Created By: Matthew
Framework Version: v1.2.1
Last Updated: February 12, 2020
Created On: October 12, 2019

Please read license.txt for license information
'''
import sys
import os
import datetime
import time
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
from util import config, startupchecks, commandchecks, logger, dbQuery, dbInsert


# gets prefix for bot
def get_prefix(bot, message):
    return dbQuery.prefix(message.guild.id)  # returns prefix


conf = config.readINI('mainConfig.ini')  # loads config
botName = conf['main']['botname']  # gets bots name from config
# gets bots prefix and case_insensitivity
bot = commands.Bot(command_prefix=get_prefix, case_insensitive=True)


# startupLog (command)
@bot.command(name='startupLog', description='prints startup-log.txt', usage='outputLog', aliases=['outlog', 'output', 'oplog', 'log'])
@commands.is_owner()
async def startupLog(ctx):
    # sends startup-log.txt
    await ctx.send(f"```{logger.output('startup-log.txt')}```")


# on startup
@bot.event
async def on_ready():
    startTime = time.time()

    # wipes all logs
    logger.wipe('startup-log.txt')
    logger.wipe('runtime-log.txt')
    logger.infoStart('Running Checks')

    # runs startup checks that are in startupchecks.py
    if startupchecks.startUpChecks() is False:
        logger.errorStart("Something isn't configured correctly for startup")
        logger.errorStart("Startup aborted")
    else:
        # writes startup information to startup-log.txt
        logger.write('startup-log.txt', f'Starting {botName}', "[info]", "\n")
        logger.infoStart(f'discord.py {discord.__version__}')
        logger.infoStart(f'Python {sys.version[:6]}')

        # Requires Cogs loading
        # Any file in /cogs/required is considered a required cog
        # These files must ALL be loaded in order for the bot to continue initializing
        logger.write('startup-log.txt', 'Initializing Required Cogs', "[info]", "\n")
        for required in os.listdir('./cogs/required'):
            if required.endswith('.py'):
                try:
                    bot.load_extension(f'cogs.required.{required[:-3]}')
                    logger.passStart(f'{required}')
                except Exception as e:
                    logger.errorStart(f'{required}')
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
        for cog in os.listdir(f'./cogs/main'):
            if cog.endswith('.py'):
                try:
                    value = dbQuery.cog(cog[:-3])
                    if value != True and value != False:
                        dbInsert.cogs(cog[:-3], False)
                        value = False
                except:
                    value = False
                    pass

                if value:
                    try:
                        bot.load_extension(f'cogs.main.{cog[:-3]}')
                        logger.passStart(f'{cog}')
                        countSuccess += 1
                    except Exception as e:
                        logger.errorStart(f'{cog}')
                        logger.errorStart(f'{e}')
                        countFail += 1
                else:
                    logger.skipStart(f'{cog}')
                    countSkip += 1

        logger.infoStart(f'Success: {countSuccess}  Failed: {countFail}  Skipped: {countSkip}\n')
        logger.infoStart(f'{botName} is ready to rumble!')
        logger.infoStart(f'Initialized in {int((time.time() - startTime)*1000)}ms')

# Starts bot with Discord token from mainConfig.ini
bot.run(conf['main']['discordToken'])