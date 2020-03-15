'''
Name: Leaderboard
Description: Leaderboard system
'''

import discord
from discord.ext import commands
import datetime
import time
import random
import math
from discord.ext.commands import has_permissions
from util import dbQuery, dbInsert, commandchecks, embed


class Leaderboard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        try:
            if (message.author == self.bot.user) or message.author.bot:
                return
            currentDateTime = datetime.datetime.now()
            data = dbQuery.leaderboard(message.guild.id, message.author.id)
            lastDateTime = data[5] + datetime.timedelta(seconds=60)
            if lastDateTime < currentDateTime:
                points = random.randint(15, 25) + data[4]
                level = math.floor(0.08 * math.sqrt(points)) + 1
                author = str(message.author)
                dbInsert.leaderboard(data[0], data[1], author, level, points, currentDateTime, data[6] + 1)
            else:
                return
        except:
            author = str(message.author)
            dbInsert.leaderboard(message.guild.id, message.author.id, author, 1, random.randint(15, 25), datetime.datetime.now(), 1)

    # rank (command)
    @commands.check(commandchecks.isAllowed)
    @commands.command(name="rank", description="Displays current rank.", usage="rank <user>", aliases=['xp'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def rank(self, ctx, *, user: discord.Member = None):
        try:
            if not user:
                userID = int(ctx.author.id)
                userDisplay = str(ctx.author)
            else:
                userID = int(user.id)
                userDisplay = str(user)
            data = dbQuery.leaderboard(ctx.guild.id, userID)
            await ctx.send(embed=embed.make_embed(userDisplay, f"**Level:** {data[3]}\n**XP:** {data[4]}\n**Messages:** {data[6]}"))
        except:
            await ctx.send(embed=embed.make_error_embed("User unavailable."))

def setup(bot):
    bot.add_cog(Leaderboard(bot))