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
            lastDateTime = data[7] + datetime.timedelta(seconds=60)
            if lastDateTime < currentDateTime:
                points = random.randint(15, 25) + data[5]
                level = math.floor(0.08 * math.sqrt(points)) + 1
                x = level + 1
                nextlevel = math.floor((((625*(x**2))/4)-((625*x)/2)+(625/4)) - points)
                author = str(message.author)
                dbInsert.leaderboard(data[0], message.guild.name, data[2], author, level, points, nextlevel, currentDateTime, data[8] + 1)
            else:
                return
        except:
            author = str(message.author)
            randomValue = random.randint(15, 25)
            dbInsert.leaderboard(message.guild.id, message.guild.name, message.author.id, author, 1, randomValue, 156 - randomValue, datetime.datetime.now(), 1)

    # rank (command)
    @commands.check(commandchecks.isAllowed)
    @commands.command(name="rank", description="Displays current rank.", usage="rank <user>", aliases=['xp'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def rank(self, ctx, *, user: discord.Member = None):
        try:
            if not user:
                userID = int(ctx.author.id)
                userDisplay = str(ctx.author)
                userAvatar = ctx.author.avatar
                userColor = ctx.author.color
            else:
                userID = int(user.id)
                userDisplay = str(user)
                userAvatar = user.avatar
                userColor = user.color
            data = dbQuery.leaderboard(ctx.guild.id, userID)

            if data[4] == "":
                await ctx.send(embed=embed.make_error_embed("User unavailable."))

            emb = discord.Embed(description=f"Rank Info", color=userColor)
            emb.set_author(name=userDisplay, icon_url=f'https://cdn.discordapp.com/avatars/{userID}/{userAvatar}.png', url=f'https://applesauce.site/member.php?member={userID}')
            emb.add_field(name='Level', value=data[4], inline=False)
            emb.add_field(name='Next Level XP', value=data[6], inline=False)
            emb.add_field(name='Total XP', value=data[5], inline=False)
            emb.add_field(name='Message Count', value=data[8], inline=False)
            await ctx.send(embed=emb)
        except:
            await ctx.send(embed=embed.make_error_embed("User unavailable."))

    # leaderboard (command)
    @commands.check(commandchecks.isAllowed)
    @commands.command(name="leaderboard", description="Displays link to leaderboard.", usage="leaderboard", aliases=['levels'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def leaderboard(self, ctx):
        await ctx.send(f"Leaderboard: http://applesauce.site/leaderboard.php?guild={ctx.guild.id}")

def setup(bot):
    bot.add_cog(Leaderboard(bot))