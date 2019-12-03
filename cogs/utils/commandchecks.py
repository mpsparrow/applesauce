import discord
from discord.ext import commands
from logs import logger
import json

# command check function
def allowedUser(ctx):
    ### checks if user is in ignored list
    try:
        with open(r'config.json', 'r') as file:
            user_data = json.load(file)
            ignoredUsers = user_data['ignored']['users']
        if str(ctx.author) in ignoredUsers:
            return False
    except:
        logger.outputWrite(f'Command Check Failure')

    ### checks if command is enabled in guild
    try:
        with open('commandconfig.json', 'r') as json_data_file:
            commandconfig = json.load(json_data_file)
        guildID = str(ctx.guild.id)
        name = str(ctx.command.qualified_name)
        cog = str(ctx.command.cog.qualified_name)
        try:
            value = commandconfig[guildID]
            try:
                value = commandconfig[guildID][cog]
                try:
                    value = commandconfig[guildID][cog][name]
                    return value
                except:
                    commandconfig[guildID][cog][name] = False
            except:
                commandconfig[guildID][cog] = {}
                commandconfig[guildID][cog][name] = False
        except:
            commandconfig[guildID] = {}
            commandconfig[guildID][cog] = {}
            commandconfig[guildID][cog][name] = False
        with open(r'commandconfig.json', 'w') as json_data_file:
            json.dump(commandconfig, json_data_file, indent=2)
        return False
    except:
        logger.outputWrite(f'Command Check Failure')
        return False
