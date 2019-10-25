import discord
from discord.ext import commands
from cogs import configloader
import sys
import os
import json

botName = configloader.config.get("main", "botName") # get bots name from config

print(f'Initializing {botName}.......') # console
print('Initializing Discord.py.......') # console

bot = commands.Bot(command_prefix = configloader.config['main']['prefix'])

print('Initializing Extensions.......') # console

@bot.event
async def on_ready():
    countSuccess = 0
    countFail = 0
    for extension in os.listdir('./cogs'):
        if extension.endswith('.py'):
            if extension[:-3] not in json.loads(configloader.config.get("main","excludedModules")):
                try:
                    bot.load_extension(f'cogs.{extension[:-3]}')
                    print(f'Successfully loaded {extension}')
                    countSuccess += 1
                except Exception as e:
                    print(f'Failed to load {extension}')
                    print(e)
                    countFail += 1
    print(f'Modules Loaded: Success: {countSuccess} Failed: {countFail}\n')
    print('Debug:')
    print(f'discord.py version: {discord.__version__}')
    print(f'python version: {sys.version}\n')
    print(f'{botName} is ready to rumble!\n')

bot.run(configloader.config['main']['token'])
