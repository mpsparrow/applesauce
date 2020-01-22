'''
Name: Base Converter 
Description: Commands to convert from one base to another.
Last Updated: January 22, 2020
Created: January 22, 2020
'''
import discord
from discord.ext import commands
from utils import commandchecks, embed

class BaseConvert(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.check(commandchecks.isAllowed)
    @commands.command(name="base10", description="Converts to base 10", usage="b10 <base-from> <value>", aliases=['b10'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def base10(self, ctx, baseFrom: int, numValue):
        if len(numValue) > 20 or baseFrom > 36 or baseFrom < 2:
            await ctx.send(embed=embed.make_error_embed("Value too large."))
            return
        
        alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        x = len(numValue)
        finalValue = 0
        for num in numValue:
            x = x - 1
            if num.upper() in alphabet:
                finalValue += (alphabet.index(num) + 10)*(baseFrom**x)
            else:
                finalValue += int(num)*(baseFrom**x)
        
        await ctx.send(finalValue)

def setup(bot):
    bot.add_cog(BaseConvert(bot))