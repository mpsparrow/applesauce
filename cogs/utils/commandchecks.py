import discord
from discord.ext import commands
from logs import logger
import json

# command check function
def allowedUser(ctx):
    ### checks if command is enabled in guild
    try:
        with open('guildconfig.json', 'r') as json_data_file:
            guildconfig = json.load(json_data_file)
        guildID = str(ctx.guild.id)
        name = str(ctx.command.qualified_name)
        cog = str(ctx.command.cog.qualified_name)
        try:
            value = guildconfig[guildID]
            try:
                value = guildconfig[guildID]["Commands"]
                try:
                    value = guildconfig[guildID]["Commands"][cog]
                    try:
                        value = guildconfig[guildID]["Commands"][cog][name]
                        return value
                    except:
                        guildconfig[guildID]["Commands"][cog][name] = False
                except:
                    guildconfig[guildID]["Commands"][cog] = {}
                    guildconfig[guildID]["Commands"][cog][name] = False
            except:
                guildconfig[guildID]["Commands"] = {}
        except:
            guildconfig[guildID] = {}
            guildconfig[guildID]["Commands"] = {}
            guildconfig[guildID]["Commands"][cog] = {}
            guildconfig[guildID]["Commands"][cog][name] = False
        with open(r'guildconfig.json', 'w') as json_data_file:
            json.dump(guildconfig, json_data_file, indent=2)
        return False
    except:
        logger.outputWrite(f'Command Check Failure (guild)')
        return False

    ### checks if user is in ignored list
    try:
        with open(r'config.json', 'r') as file:
            user_data = json.load(file)
        try:
            ignoredUsers = user_data[str(ctx.guild.id)]['ignored']
            if str(ctx.author) in ignoredUsers:
                return False
        except:
            pass
    except:
        logger.outputWrite(f'Command Check Failure (ignored user)')
