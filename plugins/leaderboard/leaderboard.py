import discord
import math
import random
import datetime
import pymongo
from discord.ext import commands
from utils.checks import is_guild_enabled
from utils.config import readINI
from utils.database.actions import connect
from utils.logger import pluginLog

class Leaderboard(commands.Cog):
    """
    Leaderboard system
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        try:
            # Ignore bot users
            if (message.author == self.bot.user) or message.author.bot:
                return

            authorID = message.author.id
            guildID = message.guild.id

            leaderboardCol = connect()[readINI("config.ini")["MongoDB"]["database"]]["userLeaderboard"] # connect to DB
            leaderboardObj = leaderboardCol.find_one({ "_id": authorID }) # gets users object

            # date and time variables
            currentDateTime = datetime.datetime.now() - datetime.timedelta(seconds=60)
            dateYear = datetime.datetime.now().year
            dateMonth = datetime.datetime.now().month

            if leaderboardObj is None or leaderboardObj[str(guildID)] is None:
                # create initial object
                points = random.randint(15, 25)

                guildData = { 
                                "dateTime": datetime.datetime.now(),
                                "level": 1,
                                "points": points,
                                "messages": 1,
                                "total_messages": 1,
                                str(dateYear): {
                                    str(dateMonth): {
                                        "points": points,
                                        "messages": 1,
                                        "total_messages": 1
                                    }
                                }
                            }
                leaderboardCol.update_one({ "_id": authorID }, { "$set": { f"{guildID}": guildData }}, upsert=True)
            elif leaderboardObj[str(guildID)]["dateTime"] < currentDateTime:
                # one minute has past since points were awarded
                points = random.randint(15, 25)

                leaderboardCol.update_one({ "_id": authorID }, 
                                            { "$set": { 
                                                f"{guildID}.dateTime": datetime.datetime.now(),
                                                f"{guildID}.level": math.floor(0.08 * math.sqrt(leaderboardObj[str(guildID)]["points"] + points)) + 1,
                                                f"{guildID}.points": leaderboardObj[str(guildID)]["points"] + points,
                                                f"{guildID}.messages": leaderboardObj[str(guildID)]["messages"] + 1,
                                                f"{guildID}.total_messages": leaderboardObj[str(guildID)]["total_messages"] + 1
                                            }}, upsert=True)

                if str(dateYear) not in leaderboardObj[str(guildID)]:
                    # year object
                    yearData = {
                                    str(dateMonth): {
                                        "points": points,
                                        "messages": 1,
                                        "total_messages": 1
                                    }
                            }

                    leaderboardCol.update_one({ "_id": authorID }, { "$set": { f"{guildID}.{dateYear}": yearData }}, upsert=True)
                elif str(dateMonth) not in leaderboardObj[str(guildID)][str(dateYear)]:
                    # month object
                    monthData = {
                                    "points": points,
                                    "messages": 1,
                                    "total_messages": 1
                                }

                    leaderboardCol.update_one({ "_id": authorID }, { "$set": { f"{guildID}.{dateYear}.{dateMonth}": monthData }}, upsert=True)
                else:
                    # update month object
                    leaderboardCol.update_one({ "_id": authorID }, 
                                                { "$set": { 
                                                    f"{guildID}.{dateYear}.{dateMonth}.points": leaderboardObj[str(guildID)][str(dateYear)][str(dateMonth)]["points"] + points,
                                                    f"{guildID}.{dateYear}.{dateMonth}.messages": leaderboardObj[str(guildID)][str(dateYear)][str(dateMonth)]["messages"] + 1,
                                                    f"{guildID}.{dateYear}.{dateMonth}.total_messages": leaderboardObj[str(guildID)][str(dateYear)][str(dateMonth)]["total_messages"] + 1
                                                }}, upsert=True)
            else:
                # one minute hasn't past since points were awarded
                leaderboardCol.update_one({ "_id": authorID }, { "$set": { f"{guildID}.total_messages": leaderboardObj[str(guildID)]["total_messages"] + 1 }}, upsert=True)

                if str(dateYear) not in leaderboardObj[str(guildID)]:
                    # year object
                    yearData = {
                                    str(dateMonth): {
                                        "points": 0,
                                        "messages": 0,
                                        "total_messages": 1
                                    }
                               }

                    leaderboardCol.update_one({ "_id": authorID }, { "$set": { f"{guildID}.{dateYear}": yearData }}, upsert=True)
                elif str(dateMonth) not in leaderboardObj[str(guildID)][str(dateYear)]:
                    # month object
                    monthData = {
                                    "points": 0,
                                    "messages": 0,
                                    "total_messages": 1
                                }

                    leaderboardCol.update_one({ "_id": authorID }, { "$set": { f"{guildID}.{dateYear}.{dateMonth}": monthData }}, upsert=True)
                else:
                    # update month object
                    leaderboardCol.update_one({ "_id": authorID }, { "$set": { f"{guildID}.{dateYear}.{dateMonth}.total_messages": leaderboardObj[str(guildID)][str(dateYear)][str(dateMonth)]["total_messages"] + 1 }}, upsert=True)

        except Exception as e:
            pluginLog.error(f"Leaderboard Error - USER: {message.author.id} GUILD: {message.guild.id} ERROR: {e}")

    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.command(name="rank", description="Gives current rank on the server")
    @is_guild_enabled()
    async def rank(self, ctx, *, user: discord.Member = None):
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

        try:
            leaderboardCol = connect()[readINI("config.ini")["MongoDB"]["database"]]["userLeaderboard"] # connect to DB
            leaderboardObj = leaderboardCol.find_one({ "_id": userID })[str(ctx.guild.id)] # gets users object

            emb = discord.Embed(description=f"Rank Info", color=userColor)
            emb.set_author(name=userDisplay, icon_url=f"https://cdn.discordapp.com/avatars/{userID}/{userAvatar}.png")
            emb.add_field(name="Level", value=leaderboardObj["level"], inline=False)
            emb.add_field(name="XP", value=leaderboardObj["points"], inline=False)
            await ctx.send(embed=emb)
        except Exception as error:
            await ctx.send(embed=discord.Embed(title="User unavailable.", color=0xf84722))

    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.command(name="leaderboard", description="Tells you your chances of success", aliases=["levels"])
    @is_guild_enabled()
    async def leaderboard(self, ctx):
        await ctx.send(f"_insert leaderboard link here_")