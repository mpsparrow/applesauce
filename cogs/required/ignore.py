'''
Commands to ignore members
'''
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
from cogs.utils import configloader
import json

class Ignore(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ignore member command
    @commands.command()
    @commands.is_owner()
    async def ignore(self, ctx, member : discord.Member):
        try:
            config = configloader.configLoad('guildconfig.json')
            try:
                x = config[str(ctx.guild.id)]
                try:
                    x = config[str(ctx.guild.id)]['ignored']
                except:
                    config[str(ctx.guild.id)]['ignored'] = []
            except:
                config[str(ctx.guild.id)] = {}
                config[str(ctx.guild.id)]['ignored'] = []
                configloader.configDump('guildconfig.json', config)

            if str(member) not in config[str(ctx.guild.id)]['ignored']:
                config[str(ctx.guild.id)]['ignored'].append(str(member)) # appends user id to list
            configloader.configDump('guildconfig.json', config)
            await ctx.send(f'{member} is now ignored')
        except:
            await ctx.send(f'Error ignoring member {member}') # error message

    # unignore user command
    @commands.command()
    @commands.is_owner()
    async def unignore(self, ctx, member : discord.Member):
        try:
            config = configloader.configLoad('guildconfig.json')
            userList = config[str(ctx.guild.id)]['ignored'] # gets ignored users list
            
            try:
                # removes user from list
                for item in range(0, len(userList)):
                    if str(member) == userList[item]:
                        userList.pop(item)
                        break
            except:
                await ctx.send(f'User {member} not found') # if user isn't in list

            config[str(ctx.guild.id)]['ignored'] = userList # saves new list to json array
            configloader.configDump('guildconfig.json', config)
            await ctx.send(f'{member} is no longer ignored')
        except:
            await ctx.send(f'Error unignoring member {member}') # error message
        
def setup(bot):
    bot.add_cog(Ignore(bot))