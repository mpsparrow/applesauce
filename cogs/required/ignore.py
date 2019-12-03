import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
import json

class Ignore(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ignore a user command
    @commands.command()
    @commands.is_owner()
    async def ignore(self, ctx, member : discord.Member):
        try:
            with open(r'config.json', 'r') as file:
                json_data = json.load(file)
                json_data['ignored']['users'].append(str(member))
            with open(r'config.json', 'w') as file:
                json.dump(json_data, file, indent=2)
        except:
            await ctx.send("error")
        
def setup(bot):
    bot.add_cog(Ignore(bot))