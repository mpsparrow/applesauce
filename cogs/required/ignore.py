import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
import json

class Ignore(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ignore user command
    @commands.command()
    @commands.is_owner()
    async def ignore(self, ctx, member : discord.Member):
        try:
            with open(r'guildconfig.json', 'r') as file: # loads json file
                json_data = json.load(file) # gets json data
            try:
                x = json_data[str(ctx.guild.id)]
                print("1")
                try:
                    x = json_data[str(ctx.guild.id)]['ignored']
                except:
                    json_data[str(ctx.guild.id)]['ignored'] = []
            except:
                json_data[str(ctx.guild.id)] = {}
                json_data[str(ctx.guild.id)]['ignored'] = []
                with open(r'guildconfig.json', 'w') as file: # opens json file
                    json.dump(json_data, file, indent=2) # writes to json file

            if str(member) not in json_data[str(ctx.guild.id)]['ignored']:
                json_data[str(ctx.guild.id)]['ignored'].append(str(member)) # appends user id to list
            with open(r'guildconfig.json', 'w') as file: # opens json file
                json.dump(json_data, file, indent=2) # writes to json file
        except:
            await ctx.send("error") # error message

    # unignore user command
    @commands.command()
    @commands.is_owner()
    async def unignore(self, ctx, member : discord.Member):
        try:
            with open(r'guildconfig.json', 'r') as file: # loads json file
                json_data = json.load(file) # gets json data
            userList = json_data[str(ctx.guild.id)]['ignored'] # gets ignored users list
            
            try:
                # removes user from list
                for item in range(0, len(userList)):
                    if str(member) == userList[item]:
                        userList.pop(item)
                        break
            except:
                await ctx.send("User not found") # if user isn't in list

            json_data[str(ctx.guild.id)]['ignored'] = userList # saves new list to json array
            with open(r'guildconfig.json', 'w') as file: # opens json file
                json.dump(json_data, file, indent=2) # writes to json file
        except:
            await ctx.send("error") # error message
        
def setup(bot):
    bot.add_cog(Ignore(bot))