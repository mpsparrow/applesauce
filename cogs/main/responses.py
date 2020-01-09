'''
Name: Responses
Description: random responses to things
Last Updated: January 9, 2020
Created: January 8, 2020
'''
import discord
from discord.ext import commands
import random

class Responses(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        # Deep Blue and bot pinged
        if ("<@!568271450176356352>" in message.content) and ("<@!657709911337074698>" in message.content):
            await message.channel.send(f"{message.author.mention} <:pinged:451198700832817202>")
            return

        # bot pinged
        if ("<@!568271450176356352>" in message.content) and (random.choice([1,2,3,4] == 1)):
            await message.channel.send(f"{message.author.mention} <:pinged:451198700832817202>")
            return

def setup(bot):
    bot.add_cog(Responses(bot))