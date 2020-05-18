'''
Bot Name: Applesauce
Created By: Matthew
Version: v2.0
Last Updated: May 18, 2020
Created On: October 12, 2019

Please read license.txt for license information
'''
import os
import sys
import time
import discord
import datetime
from discord.ext import commands
from discord.ext.commands import has_permissions
from util.checks import startup
from util.log import startLog, log
from util.db.query import queryPrefix, queryCog
from util.db.insert import insertCog

# gets prefix for bot
def get_prefix(bot, message):
    """
    Gets prefix for specific guild
    :return: Prefix to use
    """
    try:
        return queryPrefix.prefix(message.guild.id)  # returns prefix
    except PrefixError:
        pass

conf = config.readINI('mainConfig.ini')  # loads config
botName = conf['main']['botname']  # gets bots name from config
bot = commands.Bot(command_prefix=get_prefix, case_insensitive=True)

# startupLog (command)
@bot.command(name='startupLog', description='prints startup-log.txt', usage='outputLog', aliases=['outlog', 'output', 'oplog', 'log'])
@commands.is_owner()
async def startupLog(ctx):
    # sends startup-log.txt
    await ctx.send(f"```{log.read(conf['logs']['start'])}```")

# on startup
@bot.event
async def on_ready():
    startTime = time.time()

    # wipes all logs
    log.wipe(conf['logs']['start'])
    log.wipe(conf['logs']['run'])
    startLog.info('Running Checks')

    # runs startup checks that are in startupchecks.py
    if startup.checks() is False:
        startLog.error("Something isn't configured correctly for startup")
        startLog.error("Startup aborted")
    else:
        # writes startup information to startup-log.txt
        startLog.custom(f'Starting {botName}', "[info]", "\n")
        startLog.info(f'discord.py {discord.__version__}')
        startLog.info(f'Python {sys.version[:6]}')

        # Requires Cogs loading
        # Any file in /cogs/required is considered a required cog
        # These files must ALL be loaded in order for the bot to continue initializing
        startLog.custom('Initializing Required Cogs', "[info]", "\n")
        for required in os.listdir('./cogs/required'):
            if required.endswith('.py'):
                try:
                    bot.load_extension(f'cogs.required.{required[:-3]}')
                    startLog.proceed(f'{required}')
                except Exception as e:
                    startLog.error(f'{required}')
                    startLog.error(f'{e}')
                    startLog.error('Startup aborted')
                    return

        # Main loading
        # Any file in /cogs/main is considered a cog
        # These files are attempted to be loaded. If a file errors then it is skipped and initializing continues
        startLog.custom('Initializing Cogs', "[info]", "\n")
        countSuccess = 0
        countFail = 0
        countSkip = 0
        for cog in os.listdir(f'./cogs/main'):
            if cog.endswith('.py'):
                try:
                    value = queryCog.enabled(cog[:-3])
                except CogNotFound:
                    try:
                        insertCog.cog(cog[:-3], False, False)
                        value = False
                    except CogInsertFail:
                        startLog.error(f'{cog} CogInsertFail')
                        continue

                if value:
                    try:
                        bot.load_extension(f'cogs.main.{cog[:-3]}')
                        insertCog.loaded(cog[:-3], True)
                        startLog.proceed(f'{cog}')
                        countSuccess += 1
                    except Exception as e:
                        insertCog.loaded(cog[:-3], False)
                        startLog.error(f'{cog}')
                        startLog.error(f'{e}')
                        countFail += 1
                else:
                    insertCog.cog(cog[:-3], False, False)
                    startLog.skip(f'{cog}')
                    countSkip += 1

        startLog.info(f'Success: {countSuccess}  Failed: {countFail}  Skipped: {countSkip}\n')
        startLog.info(f'{botName} is ready to rumble!')
        startLog.info(f'Initialized in {int((time.time() - startTime)*1000)}ms')

# Starts bot with Discord token from mainConfig.ini
bot.run(conf['main']['discordToken'])
