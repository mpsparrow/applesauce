'''
Name: Emoji Commands
Description: Pile of commands to display emojis
Last Updated: January 12, 2020
Created: January 12, 2020
'''
import discord
from discord.ext import commands
from utils import commandchecks

class Emoji(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # hank
    @commands.check(commandchecks.isAllowed)
    @commands.command(name="hank", description="<:hank:651284638958092301>", usage="hank")
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def hank(self, ctx):
        await ctx.send('<:hank:651284638958092301>')

    # mushroom
    @commands.check(commandchecks.isAllowed)
    @commands.command(name="mushroom", description="<a:mushroomDance:659932848035463198>", usage="mushroom", aliases=['shroom'])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def mushroom(self, ctx):
        await ctx.send('<a:mushroomDance:659932848035463198>')

    # saber
    @commands.check(commandchecks.isAllowed)
    @commands.command(name="saber", description="<a:pepelightsaber:663496095065964585>", usage="saber")
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def saber(self, ctx):
        await ctx.send('<a:pepelightsaber:663496095065964585>') 

def setup(bot):
    bot.add_cog(Emoji(bot))