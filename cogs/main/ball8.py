import discord
from discord.ext import commands
from util.checks import command
import random

class ball8(commands.Cog):
    """
    Magic 8Ball commands.
    """
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

    # 8ball (command)
    @commands.check(command.isAllowed)
    @commands.command(name="8ball", description="gives a random answer completely not based on what you ask him", usage="8ball", aliases=['magicball'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def _8ball(self, ctx):
        await ctx.send(random.choice(self.ballAnswers))

def setup(bot):
    bot.add_cog(ball8(bot))