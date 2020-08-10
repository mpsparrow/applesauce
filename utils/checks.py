import pymongo
import discord
from discord.ext import commands
from utils.database.actions import connect

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
            pluginCol = connect()["applesauce"]["plugins"]
            pluginData = pluginCol.find_one({ "_id": str(ctx.command.cog).split('.')[1] })

            if pluginData["guilds"][str(ctx.guild.id)]:
                return True
            return False
        except Exception:
            return False
    return commands.check(predicate)