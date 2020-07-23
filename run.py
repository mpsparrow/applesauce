'''
Applesauce

Created By: Matthew Sparrow
Version: v2.0
Last Updated: July 22, 2020
Created On: October 12, 2019

Licensed under GPL-3.0
(license.txt for more info)
'''
import os
import argparse
import logging
import discord
import importlib
from discord.ext import commands
from utils.logger import log, startLog, cleanLogs
from utils.checks import startupchecks

# command line arguments assigning
parser = argparse.ArgumentParser(description="Applesauce - modular Discord bot framework based on discord.py")
parser.add_argument("--s", action="store_true",
                    help="Boots the bot up in safemode (doesn't load any plugins, connect to a database, or run startup checks)")
parser.add_argument("--p", action="store_true",
                    help="Skips the loading of all plugins")
args = parser.parse_args()

cleanLogs() # clears logs and creates folder structure for logs
logging.basicConfig(filename="logs/discord.log",level=logging.INFO) # system logs defined

# defines bot
bot = commands.Bot(command_prefix="a!", case_insensitive=True)

# on_ready() starts the bootup of the bot
@bot.event
async def on_ready():
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


    if not(args.p):
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

# Starts bot with Discord token from mainConfig.ini
bot.run("xxxxxxxxx")
startLog.info("Bot Started")