'''
Command to change prefix
'''
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
from cogs.utils import configloader
import json

class Prefix(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # change prefix command
    @commands.command()
    @commands.is_owner()
    async def prefix(self, ctx, prefix):
        config = configloader.configLoad('guildconfig.json') # loads guildconfig.json
        config[str(ctx.guild.id)]['prefix'] = str(prefix) # changed prefix for that guild
        configloader.configDump('guildconfig.json', config) # saves change

def setup(bot):
    bot.add_cog(Prefix(bot))