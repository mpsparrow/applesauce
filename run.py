'''
Applesauce

Created By: Matthew Sparrow (mattthetechguy)
Version: v2.0
Last Updated: August 8, 2020
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
from utils.logger import log, startLog, clearLogs, pluginLog
from utils.database.actions import connect

# command line arguments assigning
parser = argparse.ArgumentParser(description="Applesauce - modular Discord bot framework based on discord.py")
parser.add_argument("--s", action="store_true",
                    help="Boots the bot up in safemode (doesn't load any plugins, connect to a database, or run startup checks)")
parser.add_argument("--p", action="store_false",
                    help="Skips the loading of all plugins")
parser.add_argument("--c", action="store_false",
                    help="Don't clear logs on startup")
args = parser.parse_args()

if __name__ == "__main__":
    # clears all logs in "logs" folder
    if args.c:
        clearLogs()

    logging.basicConfig(filename="logs/discord.log", level=logging.INFO) # system logs defined

    # log debug information
    startLog.debug(f"discordpy: {discord.__version__}")
    startLog.debug(f"python: {sys.version[:5]}")
    startLog.debug(f"os: {sys.platform}")

    # defines bot
    bot = commands.Bot(command_prefix=readINI("config.ini")["main"]["defaultPrefix"], case_insensitive=True)

    # starting of bot
    startLog.info("Starting Bot")

    if args.s: # if safemode 
        startLog.info("Safemode Activated")
    else: # not safemode
        # startup checks
        startLog.info("Running Checks")

        if startupChecks():
            startLog.info("Startup Checks Passed")
        else:
            startLog.error("Startup Checks Failed. Startup Aborting")
            print("Startup Checks Failed")
            print("logs\startup.log")
            os._exit(1)

        # if safemode is not active
        if args.p:
            # plugin loading
            startLog.info("Starting Plugins")

            pluginCol = connect()["applesauce"]["plugins"] # connect to DB
            pluginCol.update_many({ "loaded": True }, { "$set": { "loaded": False }}) # set all plugins to not loaded

            for folder in readINI("config.ini")["main"]["pluginFolders"]:
                for plugin in next(os.walk(folder))[1]:

                    # skips '__pycache__' folder
                    if plugin == "__pycache__":
                        continue

                    # tries to load plugin
                    try:
                        i = importlib.import_module(f"plugins.{plugin}")
                        loaded = False

                        if i.LOAD_ON_START:
                            bot.load_extension(f"plugins.{plugin}")
                            loaded = True

                        pluginINFO = { "_id": plugin, 
                                        "plugin_name": i.PLUGIN_NAME,
                                        "cog_names": i.COG_NAMES,
                                        "version": i.VERSION,
                                        "author": i.AUTHOR,
                                        "description": i.DESCRIPTION,
                                        "load_on_start": i.LOAD_ON_START, 
                                        "required": i.REQUIRED,
                                        "loaded": loaded }
                        pluginCol.update_one({ "_id": plugin }, { "$set": pluginINFO }, upsert=True)
                        startLog.info(f"{plugin} (plugin.{i.PLUGIN_NAME}) | Loaded: {loaded} | Cogs: {i.COG_NAMES} | Version: {i.VERSION}")
                        pluginLog.info(f"{plugin} (plugin.{i.PLUGIN_NAME}) | Loaded: {loaded} | Cogs: {i.COG_NAMES} | Version: {i.VERSION}")
                    except commands.ExtensionNotFound:
                        # The plugin could not be found.
                        startLog.error(f"plugins.{plugin}: not found (ExtensionNotFound)")
                        pluginLog.error(f"plugins.{plugin}: not found (ExtensionNotFound)")
                    except commands.ExtensionAlreadyLoaded:
                        # The plugin was already loaded.
                        startLog.info(f"plugins.{plugin}: already loaded (ExtensionAlreadyLoaded)")
                        pluginLog.info(f"plugins.{plugin}: already loaded (ExtensionAlreadyLoaded)")
                    except commands.NoEntryPointError:
                        # The plugin does not have a setup function.
                        startLog.error(f"plugins.{plugin}: no setup function (NoEntryPointError)")
                        pluginLog.error(f"plugins.{plugin}: no setup function (NoEntryPointError)")
                    except commands.ExtensionFailed:
                        # The plugin setup function has an execution error.
                        startLog.error(f"plugins.{plugin}: execution error (ExtensionFailed)")
                        pluginLog.error(f"plugins.{plugin}: execution error (ExtensionFailed)")
                    except Exception as error:
                        bot.unload_extension(f"plugins.{plugin}")
                        startLog.error(f"plugins.{plugin}: variables not properly defined. Plugin not loaded.")
                        pluginLog.error(f"plugins.{plugin}: variables not properly defined. Plugin not loaded.")

                        if i.REQUIRED:
                            startLog.error(f"Required plugin {plugin} failed to load. Startup Aborting")
                            print("Plugin Loading Failed")
                            print("logs\startup.log | logs\plugins.log")
                            os._exit(1)
        else:
            startLog.info("Plugin Loading Skipped")

@bot.event
async def on_ready():
    startLog.info("Connected to Discord")

# Starts bot with Discord token from config.ini
bot.run(readINI("config.ini")["main"]["discordToken"])