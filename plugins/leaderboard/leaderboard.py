import discord
import random
import datetime
import pymongo
from discord.ext import commands
from utils.checks import is_guild_enabled
from utils.config import readINI
from utils.database.actions import connect

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

            leaderboardCol = connect()[readINI("config.ini")["MongoDB"]["database"]]["leaderboard"] # connect to DB
            leaderboardObj = leaderboardCol.find_one({ "_id": authorID }) # gets users object

            # date and time variables
            currentDateTime = datetime.datetime.now() - datetime.timedelta(seconds=60)
            dateYear = datetime.datetime.now().year
            dateMonth = datetime.datetime.now().month

            if leaderboardObj is None or leaderboardObj[str(guildID)] is None:
                print("object doesn't exist")
                # create initial object
                points = random.randint(15, 25)

                guildData = { 
                                "dateTime": datetime.datetime.now(),
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
                print("over a minute")
                # one minute has past since points were awarded
                points = random.randint(15, 25)

                leaderboardCol.update_one({ "_id": authorID }, 
                                            { "$set": { 
                                                f"{guildID}.dateTime": datetime.datetime.now(),
                                                f"{guildID}.points": leaderboardObj[str(guildID)]["points"] + points,
                                                f"{guildID}.messages": leaderboardObj[str(guildID)]["messages"] + 1,
                                                f"{guildID}.total_messages": leaderboardObj[str(guildID)]["total_messages"] + 1
                                            }}, upsert=True)

                if leaderboardObj[str(guildID)][str(dateYear)] is None:
                    print("no year")
                    # year object
                    yearData = {
                                    str(dateMonth): {
                                        "points": points,
                                        "messages": 1,
                                        "total_messages": 1
                                    }
                            }

                    leaderboardCol.update_one({ "_id": authorID }, { "$set": { f"{guildID}.{dateYear}": yearData }}, upsert=True)
                elif leaderboardObj[str(guildID)][str(dateYear)][str(dateMonth)] is None:
                    print("no month")
                    # month object
                    monthData = {
                                    "points": points,
                                    "messages": 1,
                                    "total_messages": 1
                                }

                    leaderboardCol.update_one({ "_id": authorID }, { "$set": { f"{guildID}.{dateYear}.{dateMonth}": monthData }}, upsert=True)
                else:
                    print("other")
                    # update month object
                    leaderboardCol.update_one({ "_id": authorID }, 
                                                { "$set": { 
                                                    f"{guildID}.{dateYear}.{dateMonth}.points": leaderboardObj[str(guildID)][str(dateYear)][str(dateMonth)]["points"] + points,
                                                    f"{guildID}.{dateYear}.{dateMonth}.messages": leaderboardObj[str(guildID)][str(dateYear)][str(dateMonth)]["messages"] + 1,
                                                    f"{guildID}.{dateYear}.{dateMonth}.total_messages": leaderboardObj[str(guildID)][str(dateYear)][str(dateMonth)]["total_messages"] + 1
                                                }}, upsert=True)
            else:
                print("under a minute")
                # one minute hasn't past since points were awarded
                leaderboardCol.update_one({ "_id": authorID }, { "$set": { f"{guildID}.total_messages": leaderboardObj[str(guildID)]["total_messages"] + 1 }}, upsert=True)
                print("uam 1")
                print(leaderboardObj[str(guildID)])
                if str(dateYear) in leaderboardObj[str(guildID)]:
                    print("no year")
                    # year object
                    yearData = {
                                    str(dateMonth): {
                                        "total_messages": 1
                                    }
                            }

                    leaderboardCol.update_one({ "_id": authorID }, { "$set": { f"{guildID}.{dateYear}": yearData }}, upsert=True)
                """
                elif leaderboardObj[str(guildID)][str(dateYear)][str(dateMonth)] is None:
                    print("no month")
                    # month object
                    monthData = {
                                    "total_messages": 1
                                }

                    leaderboardCol.update_one({ "_id": authorID }, { "$set": { f"{guildID}.{dateYear}.{dateMonth}": monthData }}, upsert=True)
                else:
                    print("other")
                    # update month object
                    leaderboardCol.update_one({ "_id": authorID }, { "$set": { f"{guildID}.{dateYear}.{dateMonth}.total_messages": leaderboardObj[str(guildID)][str(dateYear)][str(dateMonth)]["total_messages"] + 1 }}, upsert=True)
"""
        except Exception as e:
            print(f"Error: {e}")

    @commands.command(name="rank", description="Gives current rank on the server")
    @is_guild_enabled()
    async def rank(self, ctx):
        await ctx.send(f"my rank")

    @commands.command(name="leaderboard", description="Tells you your chances of success", aliases=["levels"])
    @is_guild_enabled()
    async def leaderboard(self, ctx):
        await ctx.send(f"leaderboard")