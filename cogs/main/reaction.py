'''
Name: Emoji Reactions
Description: Emoji reactions
Last Updated: January 9, 2020
Created: October 30, 2019
'''
import discord
from discord.ext import commands
from util import commandchecks, dbConnect, dbQuery

class Reaction(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

def setup(bot):
    bot.add_cog(Reaction(bot))