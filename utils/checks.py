import pymongo
import discord
from discord.ext import commands
from utils.database.actions import connect
from utils.config import readINI

def is_guild_enabled():
    """
    Custom decorator to see if guild is enabled
    """
    def predicate(ctx):
        """
        Command check to see if guild is enabled
        :param ctx:
        """
        try:
            pluginCol = connect()[readINI("config.ini")["MongoDB"]["database"]]["plugins"]
            pluginData = pluginCol.find_one({ "_id": str(ctx.command.cog).split('.')[1] })

            if pluginData["guilds"][str(ctx.guild.id)]:
                try:
                    guildCol = connect()[readINI("config.ini")["MongoDB"]["database"]]["guilds"]
                    guildData = guildCol.find_one({ "_id": str(ctx.guild.id) })
                    if guildData["ignore"][str(ctx.author.id)]:
                        return False
                    return True
                except Exception:
                    return True
            return False
        except Exception:
            return False
    return commands.check(predicate)