'''
Name: Emoji Reactions
Description: Emoji reactions
Last Updated: January 9, 2020
Created: October 30, 2019
'''
import discord
from discord.ext import commands
from utils import commandchecks, dbConnect, dbQuery

class Reaction(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # chance (command)
    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def test(self, ctx):
        '''
        dbConnect.prefix(ctx.guild.id, "!")
        dbConnect.commands(ctx.guild.id, "ball8", True, 1)
        dbConnect.ignore(ctx.guild.id, f"{ctx.message.author.id}", False)
        '''
        dbConnect.commandCount(ctx.guild.id, "ping")
        await ctx.send("worked?")

def setup(bot):
    bot.add_cog(Reaction(bot))