'''
Commands to ignore users
 *ignore/unignore
'''
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
from utils import config
import json

class Ignore(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ignore user for guild (command)
    @commands.command()
    @commands.is_owner()
    async def ignore(self, ctx, member : discord.Member):
        # loads ignore list from config
        try:
            conf = config.configLoad('guildconfig.json')
            try:
                x = conf[str(ctx.guild.id)]
                try:
                    x = conf[str(ctx.guild.id)]['ignored']
                except:
                    conf[str(ctx.guild.id)]['ignored'] = []
            except:
                conf[str(ctx.guild.id)] = {}
                conf[str(ctx.guild.id)]['ignored'] = []
                config.configDump('guildconfig.json', conf)

            # adds user to ignore list
            if str(member) not in conf[str(ctx.guild.id)]['ignored']:
                conf[str(ctx.guild.id)]['ignored'].append(str(member))
            config.configDump('guildconfig.json', conf)
            await ctx.message.add_reaction("✅") # success
        except:
            await ctx.message.add_reaction("❌") # fail

    # unignore user for guild (command)
    @commands.command()
    @commands.is_owner()
    async def unignore(self, ctx, member : discord.Member):
        # loads ignore list from config
        try:
            conf = config.configLoad('guildconfig.json')
            userList = conf[str(ctx.guild.id)]['ignored']
            
            # removes user from list
            try:
                for item in range(0, len(userList)):
                    if str(member) == userList[item]:
                        userList.pop(item)
                        break
            except:
                await ctx.message.add_reaction("❌") # if user isn't in list (fail)

            conf[str(ctx.guild.id)]['ignored'] = userList
            config.configDump('guildconfig.json', conf)
            await ctx.message.add_reaction("✅") # success
        except:
            await ctx.message.add_reaction("❌") # fail
        
def setup(bot):
    bot.add_cog(Ignore(bot))