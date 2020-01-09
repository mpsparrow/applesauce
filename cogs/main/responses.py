'''
Name: Responses
Description: random responses to things
Last Updated: January 8, 2020
Created: January 8, 2020
'''
import discord
from discord.ext import commands

class Responses(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if ("<@!568271450176356352>" in message.content) and ("<@!657709911337074698>" in message.content):
            await message.channel.send(f"Stop pinging us {message.author.mention} <:pinged:451198700832817202>")

def setup(bot):
    bot.add_cog(Responses(bot))