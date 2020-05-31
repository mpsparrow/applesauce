import discord
from discord.ext import commands
from util.checks import command
import random

class oneLine(commands.Cog):
    """
    Simple 'one-line' commands.
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.check(command.isAllowed)
    @commands.command(name="chance", description="Random integer between 0 and 100 (displayed as percent)")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def chance(self, ctx):
        """
        Command to disable a chance between 0% and 100%
        :param ctx:
        """
        await ctx.send(f'{random.randint(0, 100)}% chance')

    @commands.check(command.isAllowed)
    @commands.command(name="coin", description="Flips a coin and returns heads or tails.")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def coin(self, ctx):
        """
        Command to flip a coin
        :param ctx:
        """
        await ctx.send(random.choice(['Heads', 'Tails']))
        
    @commands.check(command.isAllowed)
    @commands.command(name="ddos", description="You ever wanted to DDoS something? Well today is your lucky day!")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def ddos(self, ctx, *, name):
        """
        Command to pretend to DDOS something
        :param ctx:
        :param name: Name of thing to be DDoS
        """
        await ctx.send(f"DDoSing {name}")

    @commands.check(command.isAllowed)
    @commands.command(name="rate", description="Random integer rating out of 10.", aliases=['rating'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def rate(self, ctx):
        """
        Command to produce a random rating between 0 and 10
        :param ctx:
        """
        await ctx.send(f'{random.randint(0,10)}/10')

def setup(bot):
    bot.add_cog(oneLine(bot))