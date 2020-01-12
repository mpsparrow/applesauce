'''
Name: Emoji Reactions
Description: Emoji reactions
Last Updated: January 9, 2020
Created: October 30, 2019
'''
import discord
from discord.ext import commands
from utils import commandchecks

class Reactions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

def setup(bot):
    bot.add_cog(Reactions(bot))