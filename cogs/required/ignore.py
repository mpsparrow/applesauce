import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
from logs import logger
from cogs.utils import configloader
import json

class Ignore(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ignore user command

def setup(bot):
    bot.add_cog(Ignore(bot))