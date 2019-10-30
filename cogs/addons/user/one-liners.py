import discord
from discord.ext import commands
import random

class Basic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # commands
    # chance command
    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def chance(self, ctx):
        await ctx.send(f'{random.randint(0, 100)}% chance')

    # coin command
    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def coin(self, ctx):
        if random.randint(0,1) == 1:
            await ctx.send('heads')
            return
        await ctx.send('tails')

    # rate command
    @commands.command(aliases=['rating'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def rate(self, ctx):
        await ctx.send(f'{random.randint(0,10)}/10')

    # table command
    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def table(self, ctx):
        await ctx.send('(╯°□°)╯︵ ┻━┻')

def setup(bot):
    bot.add_cog(Basic(bot))
