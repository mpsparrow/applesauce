'''
Applesauce

Created By: Matthew Sparrow (mattthetechguy)
Version: v2.0
Last Updated: July 29, 2020
Created On: October 12, 2019

Licensed under GPL-3.0
(LICENSE.txt for more info)

https://github.com/mpsparrow/applesauce
'''
import os
import argparse
import logging
import discord
import importlib
from discord.ext import commands
from utils.config import readINI
from utils.checks import startupchecks

# create logs folder
if not(os.path.isdir("logs")):
    os.mkdir("logs")

from utils.logger import log, startLog, clearLogs

# command line arguments assigning
parser = argparse.ArgumentParser(description="Applesauce - modular Discord bot framework based on discord.py")
parser.add_argument("--s", action="store_true",
                    help="Boots the bot up in safemode (doesn't load any plugins, connect to a database, or run startup checks)")
parser.add_argument("--p", action="store_false",
                    help="Skips the loading of all plugins")
parser.add_argument("--c", action="store_false",
                    help="Don't clear logs on startup")
args = parser.parse_args()

# clears all logs in "logs" folder
if args.c:
    clearLogs()

logging.basicConfig(filename="logs/discord.log",level=logging.INFO) # system logs defined

# defines bot
bot = commands.Bot(command_prefix=readINI("config.ini")["main"]["defaultPrefix"], case_insensitive=True)

startLog.info("Starting Bot")

# if safemode 
if args.s:
    startLog.info("Safemode Activated")
    return

# startup checks
startLog.info("Running Checks")

if startupchecks():
    startLog.info("Startup Checks Passed")
else:
    startLog.error("Startup Checks Failed, System Aborting")
    print("Startup Checks Failed")
    print("logs\startup.log")
    os._exit(1)

# if safemode is not active
if args.p:
    # plugin loading
    startLog.info("Starting Plugins")

    for folder in ["core", "plugins"]:
        for plugins in next(os.walk(folder))[1]:

            # skips '__pycache__' folder
            if plugins == "__pycache__":
                continue

            # tries to load extension
            try:
                bot.load_extension(f"plugins.{plugins}")
                i = importlib.import_module(f"plugins.{plugins}")
                startLog.info(f"Loaded: {i.PLUGIN_NAME} | Cogs: {i.COG_NAMES} | Version: {i.VERSION}")
            except commands.ExtensionNotFound:
                # The cog could not be found.
                startLog.warning(f"plugins.{plugins}: not found (ExtensionNotFound)")
            except commands.ExtensionAlreadyLoaded:
                # The cog was already loaded.
                startLog.warning(f"plugins.{plugins}: already loaded (ExtensionAlreadyLoaded)")
            except commands.NoEntryPointError:
                # The cog does not have a setup function.
                startLog.error(f"plugins.{plugins}: no setup function (NoEntryPointError)")
            except commands.ExtensionFailed:
                # The cog setup function has an execution error.
                startLog.error(f"plugins.{plugins}: execution error (ExtensionFailed)")
            except Exception as error:
                bot.unload_extension(f"plugins.{plugins}")
                startLog.error(f"plugins.{plugins}: variables not properly defined. Plugin unloaded.")
else:
    startLog.info("Plugin Loading Skipped")

@bot.event
async def on_ready():
    startLog.info("Connected")

# Starts bot with Discord token from config.ini
bot.run(readINI("config.ini")["main"]["discordToken"])