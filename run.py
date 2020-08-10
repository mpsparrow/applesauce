'''
Applesauce

Created By: Matthew Sparrow (mattthetechguy)
Version: v2.0
Last Updated: August 9, 2020
Created On: October 12, 2019

Licensed under GPL-3.0
(LICENSE.txt for more info)

https://github.com/mpsparrow/applesauce
'''
import os
import sys
import pymongo
import argparse
import logging
import discord
import importlib
from discord.ext import commands

# create logs folder
if not(os.path.isdir("logs")) and __name__ == "__main__":
    os.mkdir("logs")

from utils.config import readINI
from utils.checks import startupChecks
from utils.logger import startLog, clearLogs, pluginLog, log
from utils.database.actions import connect

# command line arguments assigning
parser = argparse.ArgumentParser(description="Applesauce - modular Discord bot framework based on discord.py")
parser.add_argument("-c", "-skipchecks", action="store_false",
                    help="skips startup checks")
parser.add_argument("-d", "-debug", action="store_true",
                    help="prints more debug information in logs")
parser.add_argument("-l", "-skipclear", action="store_false",
                    help="skips clearing logs on startup")
parser.add_argument("-o", "-outputlog", action="store_true",
                    help="outputs startup.log to console")
parser.add_argument("-p", "-skipplugins", action="store_false",
                    help="skips the loading of all plugins")
args = parser.parse_args()

if __name__ == "__main__":
    # outputs startLog (startup.log) to console
    if args.o:
        consoleLog = logging.StreamHandler()
        consoleLog.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
        startLog.addHandler(consoleLog)

    # clears all logs in "logs" folder
    if args.l:
        clearLogs()
        startLog.info("Logs Cleared")

    # starting of bot
    startLog.info("Starting Bot")

    # system logs discord.log
    if args.d:
        # debugging mode if arg
        logging.basicConfig(filename="logs/discord.log", level=logging.DEBUG, 
                            format="%(asctime)s %(levelname)s %(message)s (%(pathname)s - %(funcName)s - %(lineno)d)")
        
        # log debug information
        startLog.debug(f"python: {sys.version[:5]}")
        startLog.debug(f"os: {sys.platform}")
        startLog.debug(f"discordpy: {discord.__version__}")
        startLog.debug(f"pymongo: {pymongo.__version__}")
        startLog.debug(f"argparse: {argparse.__version__}")
        startLog.debug(f"logging: {logging.__version__}")
    else:
        logging.basicConfig(filename="logs/discord.log", level=logging.INFO, 
                            format="%(asctime)s %(levelname)s %(message)s") 

    # defines bot
    bot = commands.Bot(command_prefix=readINI("config.ini")["main"]["defaultPrefix"], case_insensitive=True)

    # startup checks
    if args.c:
        startLog.info("Running Checks")

        if startupChecks():
            startLog.info("Checks Passed")
        else:
            startLog.error("Checks Failed. Startup Aborting")
            os._exit(1)
    else:
        startLog.info("Skipped Checks")

    # plugin loading
    if args.p:
        startLog.info("Starting Plugins")

        pluginCol = connect()["applesauce"]["plugins"] # connect to DB
        pluginCol.update_many({ "loaded": True }, { "$set": { "loaded": False }}) # set all plugins to not loaded
        folder = readINI("config.ini")["main"]["pluginFolder"]

        for plugin in next(os.walk(folder))[1]:

            # skips '__pycache__' folder
            if plugin == "__pycache__":
                continue

            # tries to load plugin
            try:
                i = importlib.import_module(f"{folder}.{plugin}")
                loaded = False

                if i.LOAD_ON_START:
                    bot.load_extension(f"{folder}.{plugin}")
                    loaded = True

                pluginINFO = { "_id": plugin, 
                                "plugin_name": i.PLUGIN_NAME,
                                "cog_names": i.COG_NAMES,
                                "version": i.VERSION,
                                "author": i.AUTHOR,
                                "description": i.DESCRIPTION,
                                "load_on_start": i.LOAD_ON_START, 
                                "required": i.REQUIRED,
                                "hidden": i.HIDDEN,
                                "loaded": loaded }
                pluginCol.update_one({ "_id": plugin }, { "$set": pluginINFO }, upsert=True)
                startLog.info(f"{i.PLUGIN_NAME} ({folder}.{plugin}) | Loaded: {loaded} | Cogs: {i.COG_NAMES} | Version: {i.VERSION}")
                pluginLog.info(f"{i.PLUGIN_NAME} ({folder}.{plugin}) | Loaded: {loaded} | Cogs: {i.COG_NAMES} | Version: {i.VERSION}")
            except commands.ExtensionNotFound as error:
                # The plugin could not be found.
                startLog.error(f"{folder}.{plugin}: not found (ExtensionNotFound)")
                startLog.error(error)
                pluginLog.error(f"{folder}.{plugin}: not found (ExtensionNotFound)")
                pluginLog.error(error)
            except commands.ExtensionAlreadyLoaded as error:
                # The plugin was already loaded.
                startLog.info(f"{folder}.{plugin}: already loaded (ExtensionAlreadyLoaded)")
                startLog.error(error)
                pluginLog.info(f"{folder}.{plugin}: already loaded (ExtensionAlreadyLoaded)")
                pluginLog.error(error)
            except commands.NoEntryPointError as error:
                # The plugin does not have a setup function.
                startLog.error(f"{folder}.{plugin}: no setup function (NoEntryPointError)")
                startLog.error(error)
                pluginLog.error(f"{folder}.{plugin}: no setup function (NoEntryPointError)")
                pluginLog.error(error)
            except commands.ExtensionFailed as error:
                # The plugin setup function has an execution error.
                startLog.error(f"{folder}.{plugin}: execution error (ExtensionFailed)")
                startLog.error(error)
                pluginLog.error(f"{folder}.{plugin}: execution error (ExtensionFailed)")
                pluginLog.error(error)
            except Exception as error:
                try:
                    bot.unload_extension(f"{folder}.{plugin}")
                    startLog.error(f"{folder}.{plugin}: variables not properly defined. Plugin not loaded.")
                    startLog.error(error)
                    pluginLog.error(f"{folder}.{plugin}: variables not properly defined. Plugin not loaded.")
                    pluginLog.error(error)

                    if i.REQUIRED:
                        startLog.error(f"Required plugin {folder}.{plugin} failed to load. Startup Aborting")
                        os._exit(1)
                except Exception as error:
                    startLog.error(f"{folder}.{plugin}: {error}")
                    pluginLog.error(f"{folder}.{plugin}: {error}")
    else:
        startLog.info("Skipped Plugin Loading")

@bot.event
async def on_ready():
    # checking for if this is the first connect or a reconnect to the Discord API
    try:
        firstRun
    except NameError:
        firstRun = True

    if firstRun:
        startLog.info(f"Connected! {bot.user.name} | {bot.user.id}")
        firstRun = False
    else:
        log.info(f"Reconnected! {bot.user.name} | {bot.user.id}")

@bot.event
async def on_command(ctx):
    print(ctx.command.cog)
    print(ctx)

@bot.event
async def on_command_error(ctx, error):
    pass

# Starts bot with Discord token from config.ini
bot.run(readINI("config.ini")["main"]["discordToken"])