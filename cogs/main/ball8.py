'''
Name: 8ball
Description: not so magic 8ball command
Last Updated: January 8, 2020
Created: October 30, 2019

= Configuration =
Boot up. Add to answers list in cogconfig.json.
'''
import discord
from discord.ext import commands
from cogs.utils import commandchecks
from cogs.utils import configloader
import random

class ball8(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # answers for 8ball command
    ballAnswers = [
        'sometimes',
        'maybe',
        'no',
        'yes',
        'of course',
        'yes daddy OwO'
    ]

    # 8ball command
    @commands.check(commandchecks.isAllowed)
    @commands.command(name="8ball", description="gives a random answer completely not based on what you ask him", usage="8ball", aliases=['magicball'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def _8ball(self, ctx):
        # picks random value from ballAnswers list
        await ctx.send(random.choice(self.ballAnswers))

def setup(bot):
    bot.add_cog(ball8(bot))