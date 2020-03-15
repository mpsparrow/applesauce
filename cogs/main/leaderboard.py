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
from util import dbQuery, dbInsert


class Leaderboard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        try:
            if message.author == self.bot.user:
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

def setup(bot):
    bot.add_cog(Leaderboard(bot))