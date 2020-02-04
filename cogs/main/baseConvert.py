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

    # baseConvert (command)
    @commands.check(commandchecks.isAllowed)
    @commands.command(name="baseConvert", description="Converts from one base to another. Acceptable base range 2-36.", usage="bc <base-from> <base-to> <value>", aliases=['bc'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def baseConvert(self, ctx, baseFrom: int, baseTo: int, numValue):
        alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

        # checks if base and values are valid and within the limits
        try:
            if len(numValue) > 20:
                await ctx.send(embed=embed.make_error_embed("Value too large."))
                return
            
            if baseFrom > 36 or baseFrom < 2 or baseTo > 36 or baseTo < 2:
                await ctx.send(embed=embed.make_error_embed("Please use a base between 2 and 36."))
                return

            for i in numValue:
                if (str(i) in alphabet):
                    if ((int(alphabet.index(i)) + 10) > baseFrom):
                        await ctx.send(embed=embed.make_error_embed(f"Invalid value for base {baseFrom}."))
                        return
                try:
                    if int(i) > baseFrom:
                        await ctx.send(embed=embed.make_error_embed(f"Invalid value for base {baseFrom}."))
                        return
                except:
                    pass
        except:
            await ctx.send(embed=embed.make_error_embed("Error"))
            return
        
        # converts value to base 10
        x = len(numValue)
        base10Value = 0
        for num in numValue:
            x = x - 1
            if num.upper() in alphabet:
                base10Value += (alphabet.index(num) + 10)*(baseFrom**x)
            else:
                base10Value += int(num)*(baseFrom**x)

        # successive division to get converted value
        digits = []
        while base10Value > 0:
            digits.insert(0, base10Value % baseTo)
            base10Value = base10Value // baseTo

        # turns array of digits into proper string
        finalValue = ""
        for i in digits:
            if i > 9:
                finalValue += alphabet[i -10]
            else:
                finalValue += str(i)
        
        await ctx.send(finalValue) # prints result

def setup(bot):
    bot.add_cog(BaseConvert(bot))