import discord
from discord.ext import commands
from cogs.utils import checks
import random

class Basic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # commands
    # chance command
    @commands.check(checks.allowedGuild)
    @commands.command(name="chance", description="random percent integer between 0 and 100", usage="chance")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def chance(self, ctx):
        await ctx.send(f'{random.randint(0, 100)}% chance')

    # coin command
    @commands.check(checks.allowedGuild)
    @commands.command(name="coin", description="flips a coin and returns heads or tails", usage="coin")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def coin(self, ctx):
        await ctx.send(random.choice(['heads', 'tails']))
        
    # DDOS command
    @commands.check(checks.allowedGuild)
    @commands.command(name="ddos", description="you ever wanted to DDOS something?", usage="ddos <what-to-DDOS>")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def ddos(self, ctx, *, name):
        await ctx.send(f'{name} is being DDoSed')

    # ping command
    @commands.check(checks.allowedGuild)
    @commands.command(name="ping", description="pong", usage="ping")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def ping(self, ctx):
        await ctx.send('pong!')

    # rate command
    @commands.check(checks.allowedGuild)
    @commands.command(name="rate", description="random rating out of 10", usage="rate", aliases=['rating'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def rate(self, ctx):
        await ctx.send(f'{random.randint(0,10)}/10')

def setup(bot):
    bot.add_cog(Basic(bot))
