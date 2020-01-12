'''
Command to change prefix
'''
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
from utils import config
import json

class Prefix(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # change prefix command
    @commands.command()
    @commands.is_owner()
    async def prefix(self, ctx, prefix):
        try:
            conf = config.configLoad('guildconfig.json')
            conf[str(ctx.guild.id)]['prefix'] = str(prefix)
            config.configDump('guildconfig.json', conf)
            await ctx.message.add_reaction("✅")
        except:
            await ctx.message.add_reaction("❌")

def setup(bot):
    bot.add_cog(Prefix(bot))