'''
Name: One Line 
Description: random "one line" simple commands
Last Updated: January 12, 2020
Created: October 30, 2019
'''
import discord
from discord.ext import commands
from utils import commandchecks
import random

class oneLine(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # chance (command)
    @commands.check(commandchecks.isAllowed)
    @commands.command(name="chance", description="Random integer between 0 and 100 (displayed as percent)", usage="chance")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def chance(self, ctx):
        await ctx.send(f'{random.randint(0, 100)}% chance')

    # coin (command)
    @commands.check(commandchecks.isAllowed)
    @commands.command(name="coin", description="Flips a coin and returns heads or tails.", usage="coin")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def coin(self, ctx):
        await ctx.send(random.choice(['Heads', 'Tails']))
        
    # DDOS (command)
    @commands.check(commandchecks.isAllowed)
    @commands.command(name="ddos", description="You ever wanted to DDoS something? Well today is your lucky day!", usage="ddos <what-to-DDOS>")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def ddos(self, ctx, *, name):
        await ctx.send(f'{name} is being DDoSed')

    # ping (command)
    @commands.check(commandchecks.isAllowed)
    @commands.command(name="ping", description="pong", usage="ping")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def ping(self, ctx):
        await ctx.send('pong!')

    # rate (command)
    @commands.check(commandchecks.isAllowed)
    @commands.command(name="rate", description="Random integer rating out of 10.", usage="rate", aliases=['rating'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def rate(self, ctx):
        await ctx.send(f'{random.randint(0,10)}/10')

def setup(bot):
    bot.add_cog(oneLine(bot))