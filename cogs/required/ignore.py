'''
Commands to ignore members
'''
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
from utils import config
import json

class Ignore(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ignore member command
    @commands.command()
    @commands.is_owner()
    async def ignore(self, ctx, member : discord.Member):
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

            if str(member) not in conf[str(ctx.guild.id)]['ignored']:
                conf[str(ctx.guild.id)]['ignored'].append(str(member)) # appends user id to list
            config.configDump('guildconfig.json', conf)
            await ctx.message.add_reaction("✅")
        except:
            await ctx.message.add_reaction("❌")

    # unignore user command
    @commands.command()
    @commands.is_owner()
    async def unignore(self, ctx, member : discord.Member):
        try:
            conf = config.configLoad('guildconfig.json')
            userList = conf[str(ctx.guild.id)]['ignored'] # gets ignored users list
            
            try:
                # removes user from list
                for item in range(0, len(userList)):
                    if str(member) == userList[item]:
                        userList.pop(item)
                        break
            except:
                await ctx.send(f'User {member} not found') # if user isn't in list

            conf[str(ctx.guild.id)]['ignored'] = userList # saves new list to json array
            config.configDump('guildconfig.json', conf)
            await ctx.message.add_reaction("✅")
        except:
            await ctx.message.add_reaction("❌")
        
def setup(bot):
    bot.add_cog(Ignore(bot))